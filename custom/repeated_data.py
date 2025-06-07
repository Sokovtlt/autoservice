from account.models import Customer


def current_data(self):
    kwargs = {}
    current_user = self.request.user
    kwargs = {
        'current_user': current_user,
        # index
        'w_home': 'Home',
        'w_register_as_customer': 'Register as a customer',
        'w_become_partner': 'Become a partner',
        'w_owner': 'Owner',
        'w_my_profile': 'My profile',
        'w_sign_in': 'Sign in',
        'w_log_out': 'Log out',
        'w_make_order': 'make an order',
        # registration as a customer
        'w_registration': 'Registration',
        'w_as_customer': 'as a customer',
        'w_dashboard': 'Dashboard',
        'w_my_cars': 'My cars',
        'w_orders': 'Orders',
        'w_offers': 'Offers',
        'w_messages': 'Messages',
        'w_support': 'Support',
    }
    return kwargs


def customer_data(self):
    kwargs = {
        'w_account': 'Personal account',
    }
    current_user = self.request.user
    list_customer = Customer.objects.filter(username=current_user.username)
    if len(list_customer) > 0:
        kwargs['current_customer'] = list_customer[0]
    else:
        kwargs['current_customer'] = False
    return kwargs


def reset_password_words(self):
    context = {
        'w_enter_new_pas': 'Enter a new password',
        'w_pas_cant_similar': 'Your password can’t be too similar to your other personal information.',
        'w_pas_8_char': 'Your password must contain at least 8 characters.',
        'w_pas_cant_com': 'Your password can’t be a commonly used password.',
        'w_pas_cant_numeric': 'Your password can’t be entirely numeric.',
        'w_new_pas': 'New password',
        'w_confirm': 'Confirm password',
        'w_button': 'Change my password',
        'w_invalid_link': 'The password reset link was invalid, possibly because it has already been used. Please request a new password reset.',
        'w_pas_success': 'your password was set successfully',
        'w_login_button': 'Log in now',
    }
    return context
