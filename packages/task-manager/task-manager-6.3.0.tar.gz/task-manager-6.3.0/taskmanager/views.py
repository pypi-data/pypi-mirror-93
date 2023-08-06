# Copyright 2017 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import abort
from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_restplus import reqparse
from flask_security import current_user
from flask_security import login_required
from flask_security import permissions_required
from flask_security import permissions_accepted

from . import control, models


# Create the web blueprint
bp = Blueprint('web', __name__)


@bp.app_errorhandler(404)
def page_not_found_error(error):
    title = f'Taskmanager: 404 Not Found'
    return render_template('error/notfound.html', title=title), 404


@bp.errorhandler(403)
def forbidden_error(error):
    title = f'Taskmanager: 403 Forbidden'
    return render_template('error/forbidden.html', title=title), 404


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('/tasks')
@login_required
@permissions_accepted('task_read', 'task_read_all')
def tasks():
    get_request_parser = reqparse.RequestParser()
    get_request_parser.add_argument('project', type=str, required=False, location='args', help="Filter on project name")
    get_request_parser.add_argument('template', type=str, required=False, location='args', help="Filter on template label")
    get_request_parser.add_argument('user', type=str, required=False, location='args', help="Filter on user by id or label")
    get_request_parser.add_argument('status', type=str, required=False, location='args', help="Filter on status.")
    get_request_parser.add_argument('tag', type=str, action='append', required=False, location='args', help="Tag name or list of tag names to filter on. When multiple tag args are given AND filter logic is applied.")
    get_request_parser.add_argument('application_name', type=str, required=False, location='args', help="Filter on application name")
    get_request_parser.add_argument('offset', type=int, required=False, location='args', help="Offset for pagination")
    get_request_parser.add_argument('limit', type=int, required=False, location='args', help="Maximum number of rows returned")

    args = get_request_parser.parse_args()

    offset = args['offset'] or 0
    limit = args['limit'] or 25

    tasks, total_nr_of_tasks = control.query_tasks(
        user=args['user'] or False,  # Signal no filter if user not set
        project=args['project'],
        status=args['status'],
        template=args['template'],
        tags=args['tag'],
        application_name=args['application_name'],
        offset=offset,
        limit=limit,
        order='asc',
    )

    return render_template('tasks.html', data=tasks, offset=offset, limit=limit, total=total_nr_of_tasks)


@bp.route('/tasks/<int:id>')
@login_required
@permissions_accepted('task_read', 'task_read_all')
def task(id):
    query = models.Task.query.filter(models.Task.id == id)
    if not current_user.has_permission('task_read_all'):
        tasks_via_user_query = query.filter(models.Task.users.contains(current_user))
        tasks_via_group_query = query.filter(models.Task.users_via_group.contains(current_user))
        query = tasks_via_user_query.union(tasks_via_group_query)
    data = query.one_or_none()

    if data is None:
        abort(404)

    return render_template('task.html', data=data)


@bp.route('/taskgroups')
@login_required
@permissions_accepted('task_read', 'task_read_all')
def taskgroups():
    data = models.TaskGroup.query.order_by(models.TaskGroup.id.asc()).all()
    if data is None:
        abort(404)
    return render_template('taskgroups.html', data=data)


@bp.route('/taskgroups/<int:id>')
@login_required
@permissions_accepted('task_read', 'task_read_all')
def taskgroup(id):
    data = models.TaskGroup.query.filter(models.TaskGroup.id == id).one_or_none()
    if data is None:
        abort(404)
    return render_template('taskgroup.html', data=data)


@bp.route('/templates')
@login_required
def templates():
    data = models.TaskTemplate.query.all()
    return render_template('templates.html', data=data)


@bp.route('/templates/<int:id>')
@login_required
def template(id):
    data = models.TaskTemplate.query.filter(models.TaskTemplate.id == id).one_or_none()

    # Count the tasks per template for this user
    users = models.User.query.all()

    counts_per_user = []
    for user in users:
        tasks_via_user_query = models.Task.query.filter(models.Task.users.contains(user))
        tasks_via_group_query = models.Task.query.filter(models.Task.users_via_group.contains(user))
        all_tasks_query = tasks_via_user_query.union(tasks_via_group_query)
        template_query = all_tasks_query.filter(models.Task.template == data)

        count_data = {
            'user_id': user.id,
            'user': user.username,
            'tasks': template_query.count(),
            'tasks_queued': template_query.filter(models.Task._status == 'queued').count(),
        }
        if count_data['tasks'] > 0:
            counts_per_user.append(count_data)

    if data is None:
        abort(404)
    return render_template('template.html', data=data, counts_per_user=counts_per_user)


@bp.route('/users')
@login_required
@permissions_accepted('user_read_all')
def users():
    data = models.User.query.all()

    return render_template('users.html', data=data)


@bp.route('/users/roles')
@login_required
@permissions_accepted('roles_manage')
def userroles():
    data = models.User.query.all()
    roles = models.Role.query.order_by(models.Role.id).all()
    return render_template('userroles.html', data=data, roles=roles)


@bp.route('/users/<int:id>')
@login_required
@permissions_accepted('user_read', 'user_read_all')
def user(id):
    data = models.User.query.filter(models.User.id == id).one_or_none()
    if data is None:
        abort(404)

    if not current_user.has_permission('user_read_all'):
        # This is a normal user, so may only see own user information.
        if current_user != data:
            abort(403)

    # Count the tasks per template for this user
    templates = models.TaskTemplate.query.all()

    tasks_via_user_query = models.Task.query.filter(models.Task.users.contains(data))
    tasks_via_group_query = models.Task.query.filter(models.Task.users_via_group.contains(data))
    all_tasks_query = tasks_via_user_query.union(tasks_via_group_query)

    counts_per_template = []
    for template in templates:
        template_query = all_tasks_query.filter(models.Task.template == template)
        count_data = {
            'template_id': template.id,
            'template': template.label,
            'tasks': template_query.count(),
            'tasks_queued': template_query.filter(models.Task._status == 'queued').count(),
        }
        if count_data['tasks'] > 0:
            counts_per_template.append(count_data)

    return render_template('user.html', data=data, counts_per_template=counts_per_template)


@bp.route('/groups')
@login_required
@permissions_accepted('group_read_all')
def groups():
    data = models.Group.query.all()
    return render_template('groups.html', data=data)


@bp.route('/groups/<int:id>')
@login_required
@permissions_accepted('group_read', 'group_read_all')
def group(id):
    data = models.Group.query.filter(models.Group.id == id).one_or_none()
    if data is None:
        abort(404)

    if not current_user.has_permission('group_read_all'):
        if data not in current_user.groups:
            abort(403)

    return render_template('group.html', data=data)


@bp.route('/tags')
@login_required
@permissions_accepted('task_read', 'task_read_all')
def tags():
    data = models.Tag.query.order_by(models.Tag.id).all()
    return render_template('tags.html', data=data)


@bp.route('/tags/<int:id>')
@login_required
@permissions_accepted('task_read_all')
def tag(id):
    data = models.Tag.query.filter(models.Tag.id == id).one_or_none()
    if data is None:
        abort(404)

    return render_template('tag.html', data=data)