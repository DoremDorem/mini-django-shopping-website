from django import forms
from .models import Account
class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'Placeholder':'Enter Your Password'
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'Placeholder':'Enter Confirm Password'
    }))
    class Meta:
        model=Account
        fields=['first_name','last_name','email','phone_number','password']

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)  
        self.fields['first_name'].widget.attrs['placeholder']="First Name"
        self.fields['last_name'].widget.attrs['placeholder']="Last Name" 
        self.fields['email'].widget.attrs['placeholder']="Email Address"
        self.fields['phone_number'].widget.attrs['placeholder']="Phone Number"
        for field in self.fields:
            self.fields[field].widget.attrs['class']="form-control"
            self.fields[field].required = True 
            self.fields[field].widget.attrs.pop("required", None) 
    def clean(self):
        get_data=super(RegistrationForm,self).clean()
        password=get_data.get("password")
        confirm_password=get_data.get("confirm_password")
        if confirm_password !=password:
            raise forms.ValidationError(
                "Confirm password not match with password"
            )
             

        
