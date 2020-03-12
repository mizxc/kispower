# -*- coding: utf-8 -*-
# @Time    : 2019-12-20
# @Author  : mizxc
# @Email   : xiangxianjiao@163.com

from flask import render_template
from project.creat import create_app

app = create_app()

@app.route('/error')
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
def error(e):
    code = e.code
    if code == 404:return render_template('admin/error-404.html')
    elif code == 500:return render_template('admin/error-500.html')
    else:return render_template('admin/error-500.html')
    return render_template('admin/error-500.html')

if __name__ == '__main__':
    app.run()
