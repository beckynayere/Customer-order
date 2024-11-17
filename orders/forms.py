from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Customer,Coupon,Payment
from . models import User

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('U', 'Unisex/Parody'))

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=17)
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    phone_number = forms.CharField(
        required=True, max_length=30, label=("phone"))
    full_name = forms.CharField(required=True)
    # = forms.CharField(widget=forms.RadioSelect(choices=GENDER_CHOICES))

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, widget=forms.RadioSelect())

    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=("Password(again)"))
    class Meta:
        model = Customer
        fields = ('full_name', 'phone_number', 'birth_date', 'email', 'gender', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput()
    
    class Meta:
        model = Profile
        fields = ('profile_picture', 'first_name',
                  'last_name', 'birth_date', 'phone_number', 'email', 'gender')

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)