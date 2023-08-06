"""Module containing account management methods, such as password changing, but
not account creation (since it's too large)."""
import shlex

import pexpect

import ocflib.account.search as search
import ocflib.account.utils as utils
import ocflib.account.validators as validators
import ocflib.infra.ldap as ldap_ocf
import ocflib.misc as misc
import ocflib.misc.mail as mail

KADMIN_PATH = '/usr/bin/kadmin'


def change_password_with_staffer(username, password, principal,
                                 admin_password, comment=None):
    """Change a user's Kerberos password using kadmin and a password, subject
    to username and password validation.

    :param comment: comment to include in notification email
    """
    validators.validate_username(username)
    validators.validate_password(username, password)

    # try changing using kadmin pexpect
    cmd = '{kadmin_path} -p {principal} cpw {username}'.format(
        kadmin_path=shlex.quote(KADMIN_PATH),
        principal=shlex.quote(principal),
        username=shlex.quote(username))

    child = pexpect.spawn(cmd, timeout=10)

    child.expect("{}@OCF.BERKELEY.EDU's Password:".format(username))
    child.sendline(password)
    child.expect("Verify password - {}@OCF.BERKELEY.EDU's Password:"
                 .format(username))
    child.sendline(password)

    # now give admin principal password
    child.expect("{}@OCF.BERKELEY.EDU's Password:".format(principal))
    child.sendline(admin_password)

    child.expect(pexpect.EOF)

    output = child.before.decode('utf8')
    if 'Looping detected' in output:
        raise ValueError('Invalid admin password given.')
    elif 'kadmin' in output:
        raise ValueError('kadmin Error: {}'.format(output))

    _notify_password_change(username, comment=comment)


def change_password_with_keytab(username, password, keytab, principal, comment=None):
    """Change a user's Kerberos password using a keytab, subject to username
    and password validation.

    :param comment: comment to include in notification email
    """
    validators.validate_username(username, check_exists=True)
    validators.validate_password(username, password)

    # try changing using kadmin pexpect
    cmd = '{kadmin_path} -K {keytab} -p {principal} cpw {username}'.format(
        kadmin_path=shlex.quote(KADMIN_PATH),
        keytab=shlex.quote(keytab),
        principal=shlex.quote(principal),
        username=shlex.quote(username))

    child = pexpect.spawn(cmd, timeout=10)

    child.expect("{}@OCF.BERKELEY.EDU's Password:".format(username))
    child.sendline(password)
    child.expect("Verify password - {}@OCF.BERKELEY.EDU's Password:"
                 .format(username))
    child.sendline(password)

    child.expect(pexpect.EOF)

    output = child.before.decode('utf8')
    if 'kadmin' in output:
        raise ValueError('kadmin Error: {}'.format(output))

    _notify_password_change(username, comment=comment)


def modify_ldap_attributes(username, attributes, **kwargs):
    """Adds or modifies arbitrary attributes of a user's LDAP record subject to
    minor validation beyond the LDAP schema.

    At the moment, the only attribute that benefits from extra validation is
    the 'loginShell' attribute.
    """

    login_shell = attributes.get('loginShell', None)
    if login_shell is not None:
        if not isinstance(login_shell, str):
            raise ValueError('Login shell must be a string')

        if not misc.validators.valid_login_shell(login_shell):
            raise ValueError("Invalid login shell '{}'".format(login_shell))

    ldap_ocf.modify_ldap_entry(
        utils.dn_for_username(username),
        attributes,
        **kwargs
    )
    # TODO: Add trailing comma to **kwargs for Python 3.6+


def _notify_password_change(username, comment=None):
    """Send email about a password change.

    :param username:
    :param comment: a string to include indicating how/why the password was
                    reset

    >>> _notify_password_change('ckuehl', comment='Your password was reset in the lab.')
    """

    name = search.user_attrs(username)['cn'][0]
    body = """Howdy there {name},

Just a quick heads up that your Open Computing Facility account password was
just reset, hopefully by you.
{comment_line}
As a reminder, your OCF username is: {username}

If you're not sure why this happened, please reply to this email ASAP.

{signature}""".format(
        name=name,
        username=username,
        signature=mail.MAIL_SIGNATURE,
        comment_line=('\n' + comment + '\n') if comment else '',
    )

    mail.send_mail_user(username, '[OCF] Account password changed', body)
