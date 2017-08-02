#coding:utf8
from django import forms

# 创建评论表单
class CommentForm(forms.Form):
    '''
    评论表单
    '''
    author = forms.CharField(widget=forms.TextInput(attrs={'id':'author','class':'comment_input','required':'required','size':'25','tabindex':'1',}),
                             max_length=50,
                             )
    comment = forms.CharField(widget=forms.Textarea(attrs={"id":"comment","class": "message_input","required": "required", "cols": "25","rows": "5", "tabindex": "2"}),)

    aid = forms.CharField(widget=forms.HiddenInput())