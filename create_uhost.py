from flask import (
    Blueprint, render_template,request
)

bp = Blueprint('create_uhost', __name__)





from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField,SelectField
from wtforms.validators import DataRequired, EqualTo

from .create_uhost_modus001 import create_effective
from .web_create_host import requesturl
from .jumpserver_user_delete import delete_user

class LoginForm(FlaskForm):
    uhostname = StringField('主机名称', validators=[DataRequired()])
    uhostcpu = IntegerField('CPU配置', validators=[DataRequired()])
    uhostmem = IntegerField('内存配置', validators=[DataRequired()])
    uhostdisk = IntegerField('磁盘配置', validators=[DataRequired()])
    uhostzone = SelectField ('北京二可用区', choices=[
        ('cn-bj2-02', u'可用区B'),
        ('cn-bj2-03', u'可用区C'),
        ('cn-bj2-04', u'可用区D'),
        ('cn-bj2-05', u'可用区E')
        ])

    uhostvpc = SelectField('VPC选择', choices=[
        ('uvnet-w4ciux', '默认vpc'),
        ('uvnet-in1py2', '运维公共'),
        ('uvnet-jfjxbh', '预发主机层'),
        ('uvnet-zpjf1w', '预发DB层'),
        ('uvnet-sh4e0x', '测试环境'),
        ('uvnet-4gc02lrd', 'K8S测试')
  ])

    uhostsystem = SelectField('系统版本选择', choices=[
        ('uimage-hlf5rp','centos7'),
        ('uimage-3n0bue','centos6')
        ])


    submit = SubmitField('开始创建')


@bp.route('/create_host/', methods = ['GET','POST'])
def create_host():
    mylist = ['恭','喜','发','财']

    form = LoginForm()

    if request.method == 'POST':
        uhostname = request.form.get('uhostname')
        uhostcpu = request.form.get('uhostcpu')
        uhostmem = int(request.form.get('uhostmem'))
        uhostdisk = request.form.get('uhostdisk')
        uhostzone = request.form.get('uhostzone')
        uhostvpc = request.form.get('uhostvpc')
        uhostsystem = request.form.get('uhostsystem')

        subnetvalue = {
            'uvnet-w4ciux': 'subnet-5dc25p',
            'uvnet-in1py2': 'subnet-uswikn',
            'uvnet-jfjxbh': 'subnet-tskjmm',
            'uvnet-zpjf1w': 'subnet-rvls5v',
            'uvnet-sh4e0x': 'subnet-ijfoof',
            'uvnet-4gc02lrd': 'subnet-z4cupqgf'
        }

        uhostnetid = subnetvalue[uhostvpc]

        if form.validate_on_submit():
            value = len(str(uhostmem))
            if value == 1:uhostmem = uhostmem * 1024

            requesturl(uhostname, uhostcpu, uhostmem, uhostdisk, uhostzone, uhostvpc, uhostnetid, uhostsystem)

            return '成功'
        else:
            return ('参数有误')

    return render_template('create_host/create_host.html', form=form, mylist=mylist)






# class DeForm(FlaskForm):
#     deleteuser = StringField('要禁用的用户名称', validators=[DataRequired()])
#
#     submit = SubmitField('执行禁用')
#
# @bp.route('/delete_user/', methods=['GET', 'POST'])
# def delete_user():
#         form = DeForm()
#         if request.method == 'POST':
#             deleteuser = request.form.get('deleteuser')
#
#         if form.validate_on_submit():
#            delete_user(deleteuser)
#            return '成功'
#         else:
#             return ('参数有误')
#         return render_template('create_host/create_host.html', form=form)




    # return render_template('create_host/create_host.html', mylist=mylist)



@bp.route('/boots/')
def boots():
    mylist = ['恭','喜','发','财']



    # return render_template('create_host/boots-them.html')
    return render_template('sky.html')


@bp.route('/')
def boots_test():
    return render_template('create_host/boots-test.html')






@bp.route("/btest/", methods=['POST','GET'])
def btest():
    mylist = ['测','试','跳','转']




    return render_template('blog/test.html', mylist=mylist)



