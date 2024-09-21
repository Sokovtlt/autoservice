from account.models import Customer


def current_data(self):
    kwargs = {}
    current_user = self.request.user
    kwargs['current_user'] = current_user
    # index
    kwargs['w_home'] = 'Home'
    kwargs['w_register_as_customer'] = 'Register as a customer'
    kwargs['w_become_partner'] = 'Become a partner'
    kwargs['w_owner'] = 'Owner'
    kwargs['w_my_profile'] = 'My profile'
    kwargs['w_sign_in'] = 'Sign in'
    kwargs['w_log_out'] = 'Log out'
    kwargs['w_make_order'] = 'make an order'
    # registration as a customer
    kwargs['w_registration'] = 'Registration'
    kwargs['w_as_customer'] = 'as a customer'
    kwargs['w_dashboard'] = 'Dashboard'
    kwargs['w_my_cars'] = 'My cars'
    kwargs['w_orders'] = 'Orders'
    kwargs['w_offers'] = 'Offers'
    kwargs['w_messages'] = 'Messages'
    kwargs['w_support'] = 'Support'
    # owner = AdministratorOwner.objects.filter(pk=current_user.id)
    # if len(owner) != 0:
    #     if owner[0].admin_owner:
    #         kwargs['owner'] = True
    # support = AdministratorSupport.objects.filter(pk=current_user.id)
    # if len(support) != 0:
    #     if support[0].admin_support:
    #         kwargs['support'] = 'Dashboard'
    return kwargs


def customer_data(self):
    customer_kwargs = {}
    current_user = self.request.user
    list_customer = Customer.objects.filter(username=current_user.username)
    if len(list_customer) > 0:
        customer_kwargs['current_customer'] = list_customer[0]
    else:
        customer_kwargs['current_customer'] = False
    return customer_kwargs
