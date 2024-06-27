from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=50, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class CouponApplyForm(forms.Form):
    code = forms.CharField(label='Coupon', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
