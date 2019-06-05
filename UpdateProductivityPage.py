#!/usr/bin/python
from wordpress_xmlrpc import Client, WordPressPost, WordPressPage
from wordpress_xmlrpc.methods.posts import GetPosts, EditPost, DeletePost
from taskw import TaskWarrior
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media

w = TaskWarrior()
tasks = w.load_tasks()
def getUrgency(task):
	return(task['urgency'])
pending = tasks['pending']
pending.sort(key=getUrgency, reverse=True)
    
content = '<strong><a href="https://spatialawareness.blog/2019/06/05/24670">What is this?</a></strong>\n\n'
content += '<strong> Most Urgent Tasks </strong>\n\n'
count = 0
for task in pending:
	if ('tags' in task and 'hide' in task['tags']) or (task['status'] == 'waiting'):
		continue
	if 'description' not in task:
		continue	
	desc = task['description']
	if 'recur' in task:
		desc = '<span style="color: #800000;">' + desc + '</span>'
	if 'depends' in task:
		desc = '<span style="color: #000080;">' + desc + '</span>'
	content += desc + '\n'
	count += 1
	if count > 9:
		break

content += '\n Recurring tasks are <span style="color: #800000;">red</span> and tasks having dependencies are <span style="color: #000080;">blue</span>.'

wp = Client('https://spatialawareness.blog/xmlrpc.php', 'username', 'password')

filename = '/home/akara/Dropbox/spatialawareness/images/TaskSummary30Days.png'
data = {
    'name' : 'TaskSummary30Days.png',
    'type' : 'image/png',
} 

with open(filename, 'rb') as img:
    data['bits'] = xmlrpc_client.Binary(img.read())

response = wp.call(media.UploadFile(data))
id30 = response['attachment_id']

with open('/home/akara/Dropbox/scripts/oldID30','r') as idno:
    wp.call(DeletePost(idno.read()))


with open('/home/akara/Dropbox/scripts/oldID30','w') as idno:
    idno.write(id30)


filename = '/home/akara/Dropbox/spatialawareness/images/TaskSummaryForever.png'
data = {
    'name' : 'TaskSummaryForever.png',
    'type' : 'image/png',
} 

with open(filename, 'rb') as img:
    data['bits'] = xmlrpc_client.Binary(img.read())

response = wp.call(media.UploadFile(data))
idf = response['attachment_id']
with open('/home/akara/Dropbox/scripts/oldIDF','r') as idno:
    wp.call(DeletePost(idno.read()))

with open('/home/akara/Dropbox/scripts/oldIDF','w') as idno:
    idno.write(idf)


chartstr = '[gallery ids ="' + id30 + ',' + idf + '" size="full" columns="1"]\n'
content2 = content + chartstr
pages = wp.call(GetPosts({'post_type': 'page'}, results_class=WordPressPage))
page = None
for pg in pages:
    if pg.id == '26':
        page = pg

page.id
page.content = content2
wp.call(EditPost(page.id, page))

