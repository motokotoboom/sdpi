from flask import Flask
import docker
from flask import request,render_template,redirect
from flask_bootstrap import Bootstrap
from threading import Thread
import queue
client = docker.from_env()
APIClient = docker.APIClient(base_url='unix://var/run/docker.sock',timeout=2)
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/services')
def services():
    services =  client.services.list()
    print ([s.id for s in services])
    return render_template('service/index.html',services=services)


@app.route('/services/<string:serviceId>',methods = ['GET', 'POST'])
def serviceContainers(serviceId):
    
    service = client.services.get(service_id=serviceId)
    
    if request.method == 'POST':
        replicas = int( request.form['replicas'])        
        mode = docker.types.ServiceMode('replicated', replicas=replicas)
        service.update(mode=mode)
        return redirect("/services", code=302)

    tasks = service.tasks()
    return render_template('container/index.html',containers=tasks)
    
@app.route('/containers')
def container():
    return 'Container list'

@app.route('/containers/<string:containerId>')
def containerDetails(containerId):
    container = client.containers.get(containerId)
    return render_template('container/details.html',container=container)

def getLogs (g,l):
    for logItem in g:
        l.append(logItem.decode())
 
    

@app.route('/services/<string:serviceId>/logs/<string:containerId>')
def containerLogs(serviceId,containerId):

    allLogs = []
    logs = []
    logQueue = queue.Queue()
    serviceLogs = APIClient.service_logs(serviceId,stdout=True,details=True,follow=False)
    print ('trying to get logs')
    t = Thread(target=getLogs,args=(serviceLogs,allLogs))
    t.daemon = True
    t.start()
    t.join(1)
    if t.is_alive():
        print ('Timeout')

    for l in allLogs:
        print (l)
        if containerId[:11] in l:
            logs.append(l)

    return render_template('service/logs.html',logs=logs)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
