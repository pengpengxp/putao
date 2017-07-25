# -*- coding: utf-8; -*-
import csv
import json
import logging
import uuid
import time

from django.db import connection
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext


logging.basicConfig(filename='/tmp/debug.log', level=logging.DEBUG)


def hello(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute('select id,name,count,pay_state,take,desc from tb;')
        user = [
            {'id': u[0],
             'name': u[1],
             'count': u[2],
             'pay_state': u[3],
             'take': u[4],
             'desc': u[5]} for u in cursor.fetchall()]

        return render_to_response('main.html',
                                  {
                                      'user': user,
                                      'guser': json.dumps(user),
                                  },
                                  context_instance=RequestContext(request))
    else:
        pass


def new(request):
    if request.method == 'GET':
        return render_to_response('new.html',
                                  {},
                                  context_instance=RequestContext(request))
    else:
        logging.debug('post data = %s' % request.POST)
        name = unicode( request.POST.get('name')).encode('utf-8')
        count = request.POST.get('count')
        pay_state = request.POST.get('pay_state')
        take = request.POST.get('take')
        desc = unicode(request.POST.get('desc')).encode('utf-8')
        cursor = connection.cursor()
        id = 'testid'
        id = uuid.uuid1()

        sql_cmd = 'insert into tb values("{}","{}", "{}", "{}", "{}", "{}");'.format(id,
                                                                                     name,
                                                                                     count,
                                                                                     pay_state,
                                                                                     take,
                                                                                     desc)
        cursor.execute(sql_cmd)
        cursor.execute('')

        return HttpResponseRedirect('/',
                                    content_type='application/json')


def change(request):
    if request.method == 'GET':
        pass
    else:
        logging.debug('post data = %s' % request.POST)
        action = request.POST.get('action')

        id = request.POST.get('id')
        cursor = connection.cursor()

        if action == 'MODIFY':
            logging.debug('action = %s, id = %s' % (action, id))
            name = unicode(request.POST.get('name')).encode('utf-8')
            count = request.POST.get('count')
            pay_state = request.POST.get('pay_state')
            take = request.POST.get('take')
            desc = unicode(request.POST.get('desc')).encode('utf-8')
            sql_cmd = 'update tb set name="{}",count="{}",pay_state="{}",take="{}",desc="{}" where id="{}";'.format(name,
                                                                                                                    count,
                                                                                                                    pay_state,
                                                                                                                    take,
                                                                                                                    desc,
                                                                                                                    id)
            cursor.execute(sql_cmd)
        elif action == 'DELETE':
            logging.debug('action = %s, id = %s' % (action, id))
            sql_cmd = 'delete from tb where id == "{}";'.format(id)
            cursor.execute(sql_cmd)

        return HttpResponseRedirect('/',
                                    content_type='application/json')


def export_win(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute('select id,name,count,pay_state,take,desc from tb;')
        user = [
            {'id': u[0],
             'name': u[1],
             'count': u[2],
             'pay_state': u[3],
             'take': u[4],
             'desc': u[5]} for u in cursor.fetchall()]

        response = HttpResponse(content_type='text/csv')
        filename = time.strftime("%d/%m/%Y") + '-putao.csv'
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

        writer = csv.writer(response)
        header = [u'用户名',
                  u'数量（斤）',
                  u'支付状态',
                  u'取货状态',
                  u'备注',
                  u'操作',
        ]
        header = [item.encode('gb2312') for item in header]
        writer.writerow(header)
        for u in user:
            temp = [unicode(u['name']),
                    unicode(u['count']),
                    unicode(u['pay_state']),
                    unicode(u['take']),
                    unicode(u['desc']),
            ]
            writer.writerow([item.encode('gb2312') for item in temp])
        return response
    else:
        pass


def export(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute('select id,name,count,pay_state,take,desc from tb;')
        user = [
            {'id': u[0],
             'name': u[1],
             'count': u[2],
             'pay_state': u[3],
             'take': u[4],
             'desc': u[5]} for u in cursor.fetchall()]

        response = HttpResponse(content_type='text/csv')
        filename = time.strftime("%d/%m/%Y") + '-putao.csv'
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

        writer = csv.writer(response)
        header = [u'用户名',
                  u'数量（斤）',
                  u'支付状态',
                  u'取货状态',
                  u'备注',
                  u'操作',
        ]
        header = [item.encode('utf8') for item in header]
        writer.writerow(header)
        for u in user:
            temp = [unicode(u['name']),
                    unicode(u['count']),
                    unicode(u['pay_state']),
                    unicode(u['take']),
                    unicode(u['desc']),
            ]
            writer.writerow([item.encode('utf8') for item in temp])
        return response
    else:
        pass
