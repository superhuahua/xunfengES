#coding: utf8
from functools import wraps
from flask import session,url_for, redirect,logging

# 登录状态检查
def logincheck(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            if session.has_key('login'):
                if session['login'] == 'loginsuccess':
                    return f(*args, **kwargs)
                else:
                    return redirect(url_for('Login'))
            else:
                return redirect(url_for('Login'))
        except Exception, e:
            print e
            return redirect(url_for('Error'))

    return wrapper


# 检查referer
def anticsrf(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            if request.referrer and request.referrer.replace('http://', '').split('/')[0] == request.host:
                return f(*args, **kwargs)
            else:
                return redirect(url_for('NotFound'))
        except Exception, e:
            print e
            return redirect(url_for('Error'))

    return wrapper