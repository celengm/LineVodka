# -*- coding: utf-8 -*-
from LineAlpha import LineClient
from LineAlpha.LineApi import LineTracer
from LineAlpha.LineThrift.ttypes import Message
from LineAlpha.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient() 
client._tokenLogin("EmYYHkG0w3eQblNMamRd.6AZ1bvq+KAa4D/tcvGksdq.YLVXyISIJkggWVCm9LfAC4biYhyf9B/wAcQWhWHC0QU=")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()


wait = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
   }

setTime = {}
setTime = wait["setTime"]

wait2 = {    
    'message':"Thanks for add me,My Creator Http://line.me/ti/p/~lianekof" 
    }

def sendMessageWithMention(self, to, text='', data=[]):
    arr = []
    list_text=''
    if '[list]' in text.lower():
        i=0
        for l in data:
            list_text+='\n@[list-'+str(i)+']'
            i=i+1
        text=text.replace('[list]', list_text)
    elif '[list-' in text.lower():
        text=text
    else:
        i=0
        for l in data:
            list_text+=' @[list-'+str(i)+']'
            i=i+1
        text=text+list_text
    i=0
    for l in data:
        mid=l[0]
        name='@[list-'+str(i)+']'
        ln_text=text.replace('\n',' ')
        length_n=len(name)
        if ln_text.find(name):
            line_s=int( ln_text.index(name) )
            line_e=(int(line_s)+int(length_n))
        arrData={'S': str(line_s), 'E': str(line_e), 'M': mid}
        arr.append(arrData)
        i=i+1
    contentMetadata={'MENTION':str('{"MENTIONEES":' + json.dumps(arr).replace(' ','') + '}')}
    return self.sendMessage(to, text, contentMetadata)
        
def sendImage(self, to_, path):
    M = Message(to=to_, text=None, contentType = 1)
    M.contentMetadata = None
    M.contentPreview = None
    M2 = self._client.sendMessage(0,M)
    M_id = M2.id
    files = {
        'file': open(path, 'rb'),
    }
    params = {
        'name': 'media',
        'oid': M_id,
        'size': len(open(path, 'rb').read()),
        'type': 'image',
        'ver': '1.0',
    }
    data = {
        'params': json.dumps(params)
    }
    r = self.post_content('https://obs-sg.line-apps.com/talk/m/upload.nhn', data=data, files=files)
    if r.status_code != 201:
        raise Exception('Upload image failure.')
    return True

def sendImage2(self, to_, path):
    M = Message(to=to_,contentType = 1)
    M.contentMetadata = None
    M.contentPreview = None
    M_id = self._client.sendMessage(M).id
    iles = {
        'file': open(path, 'rb'),
    }
    params = {
        'name': 'media',
        'oid': M_id,
        'size': len(open(path, 'rb').read()),
        'type': 'image',
        'ver': '1.0',
    }
    data = {
        'params': json.dumps(params)
    }
    r = self._client.post_content('https://os.line.naver.jp/talk/m/upload.nhn', data=data, files=files)
    if r.status_code != 201:
        raise Exception('Upload image failure.')
    return True

def sendImageWithURL(self, to_, url):
    path = '%s/pythonLine-%i.data' % (tempfile.gettempdir(), randint(0, 9))
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'w') as f:
            shutil.copyfileobj(r.raw, f)
    else:
        raise Exception('Download image failure.')
    try:
        self.sendImage(to_, path)
    except:
        try:
            self.sendImage(to_, path)
        except Exception as e:
            raise e
            
def cloneContactProfile(self, mid):
    contact = self.getContact(mid)
    profile = self.profile
    profile.displayName = contact.displayName
    profile.statusMessage = contact.statusMessage
    profile.pictureStatus = contact.pictureStatus
    self.updateProfilePicture(profile.pictureStatus)
    return self.updateProfile(profile)

def updateProfilePicture(self, hash_id):
    return self._client.updateProfileAttribute(0, 8, hash_id)
        
def mention(to,nama):
    aa = ""
    bb = ""
    strt = int(12)
    akh = int(12)
    nm = nama
    print nm
    for mm in nama:
      akh = akh + 2
      aa += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(mm)+"},"""
      strt = strt + 6
      akh = akh + 4
      bb += "\xe2\x98\xbb @x \n"
    aa = (aa[:int(len(aa)-1)])
    msg = Message()
    msg.to = to
    msg.from_ = profile.mid
    msg.text = "「Sider」\n"+bb
    msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+aa+']}','EMTVER':'4'}
    print msg
    try:
       client.sendMessage(msg)
    except Exception as error:
        print error
        
def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)

def NOTIFIED_READ_MESSAGE(op):
    #print op
    try:
        if op.param1 in wait['readPoint']:
            Name = client.getContact(op.param2).displayName
            if Name in wait['readMember'][op.param1]:
                pass
            else:
                wait['readMember'][op.param1] += "\n・" + Name
                wait['ROM'][op.param1][op.param2] = "・" + Name
        else:
            pass
    except:
        pass

tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.to in wait['readPoint']:
                    if msg.from_ in wait["ROM"][msg.to]:
                        del wait["ROM"][msg.to][msg.from_]
                else:
                    pass
            except:
                pass
        else:
            pass
    except KeyboardInterrupt:
	       sys.exit(0)
    except Exception as error:
        print error
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

def SEND_MESSAGE(op):
    msg = op.message
    try:
        if msg.toType == 0:
            if msg.contentType == 0:
                if msg.text == "Mid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "Me":
                    sendMessage(msg.to, text=None, contentMetadata={'mid': msg.from_}, contentType=13)
                if msg.text == "Gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text in ["Sp","Speed","speed"]:
                    start = time.time()
                    sendMessage(msg.to, text="Waiting...", contentMetadata=None, contentType=None)
                    elapsed_time = time.time() - start
                    sendMessage(msg.to, "%sseconds" % (elapsed_time))
                if msg.text == "Time":
                   sendMessage(msg.to, "Sekarang " + datetime.datetime.today().strftime('Tanggal : %Y:%m:%d \nSekarang Jam : %H:%M:%S'))
                if msg.text == "Ginfo":
                    group = client.getGroup(msg.to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "Error"
                    md = "[Nama Grup : ]\n" + group.name + "\n\n[Id Grup : ]\n" + group.id + "\n\n[Pembuat Grup :]\n" + gCreator + "\n\n[Gambar Grup : ]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\nKode Url : Diizinkan"
                    else: md += "\n\nKode Url : Diblokir"
                    if group.invitee is None: md += "\nJumlah Member : " + str(len(group.members)) + " Orang" + "\nUndangan Yang Belum Diterima : 0 Orang"
                    else: md += "\nJumlah Member : " + str(len(group.members)) + " Orang" + "\nUndangan Yang Belum Diterima : " + str(len(group.invitee)) + " Orang"
                    sendMessage(msg.to,md)
                if msg.text == "Uni":
		            sendMessage(msg.to,"Hai Perkenalkan.....\nNama saya siapa ya?\n\n1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1\n\nMakasih Sudah Dilihat :)\nJangan Dikick ampun mzz :v")
                elif "Copy @" in msg.text:
                     _name = msg.text.replace("Copy @","")
                     _nametarget = _name.rstrip('  ')
                     gs = client.getGroup(msg.to)
                     targets = []
                     for g in gs.members:
                         if _nametarget == g.displayName:
                             targets.append(g.mid)
                     if targets == []:
                         sendMessage(msg.to, "Target Not Found")
                     else:
                         for target in targets:
                             try:
                                client.cloneContactProfile(target)
                                sendMessage(msg.to, "Succes")
                             except Exception as error:
                                 print error
                elif "Steal @" in msg.text:          
                   _name = msg.text.replace("Steal @","")
                   _nametarget = _name.rstrip('  ')
                   gs = client.getGroup(msg.to)
                   targets = []
                   for g in gs.members:
                       if _nametarget == g.displayName:
                           targets.append(g.mid)
                   if targets == []:
                       sendMassage(msg.to,"Contact not found")
                   else:
                       for target in targets:
                           try:
                               contact = client.getContact(target)
                               path = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                               client.sendImageWithURL(msg.to, path)
                           except:
                               pass
                elif "Cover @" in msg.text:          
                   _name = msg.text.replace("Cover @","")
                   _nametarget = _name.rstrip('  ')
                   gs = client.getGroup(msg.to)
                   targets = []
                   for g in gs.members:
                       if _nametarget == g.displayName:
                           targets.append(g.mid)
                   if targets == []:
                       sendMassage(msg.to,"Contact not found")
                   else:
                       for target in targets:
                           try:
                               contact = client.channel.getContact(cover)
                               path = contact.pictureStatus
                               client.sendImageWithURL(msg.to, path)
                           except:
                               pass
                if msg.text in ["Leave"]:
                    ginfo = client.getGroup(msg.to)
                    try:
                        client.leaveGroup(msg.to)
                    except:
                          pass
                if msg.text == "Sundala":
                    print "ok"
                    _name = msg.text.replace("Sundala","")
                    gs = client.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        sendMessage(msg.to,"error")
                    else:
                        for target in targets:
                            try:
                                klist=[client]
                                kicker=random.choice(klist)
                                kicker.kickoutFromGroup(msg.to,[target])
                                print (msg.to,[g.mid])
                            except:
                                sendText(msg.to,"error")
                if msg.text in ["Gclist","List gc","List groupGc list"]:              
                     gid = client.getGroupIdsJoined()
                     h = ""
                     for i in gid:
                         h += "[✞]%s\n" % (client.getGroup(i).name   + " : " + str (len (client.getGroup(i).members)))
                     sendMessage(msg.to,"========[List Group]========\n"+ h +"Total Group :" +str(len(gid)))
                if msg.text in["Summon"]:
	                group = client.getGroup(msg.to)
	                nama = [contact.mid for contact in group.members]
	                nm1, nm2, nm3, jml = [], [], [], len(nama)
	                if jml <= 100:
	                   mention(msg.to, nama)
	                if jml > 100 and jml < 200:
	                   for i in range(0, 99):
	                       nm1 += [nama[i]]
	                   mention(msg.to, nm1)
	                   for j in range(100, len(nama)-1):
	                       nm2 += [nama[j]]
	                   mention(msg.to, nm2)
	                if jml > 200  and jml < 300:
	                   for i in range(0, 99):
	                       nm1 += [nama[i]]
	                   mention(msg.to, nm1)
	                   for j in range(100, 199):
	                       nm2 += [nama[j]]
	                   mention(msg.to, nm2, jml)
	                   for k in range(200, len(nama)-1):
	                       nm3 += [nama[k]]
	                   mention(msg.to, nm3, jml)
	                if jml > 300:
	                    print "Terlalu Banyak Men 300+"
	                cnt = Message()
	                cnt.text = "Done:"+str(jml)
	                cont.to = msg.to
	                client.sendMessage(cnt)
                elif "Ratakan" in msg.text:
                       nk0 = msg.text.replace("Ratakan","")
                       nk1 = nk0.lstrip()
                       nk2 = nk1.replace("all","")
                       nk3 = nk2.rstrip()
                       _name = nk3
                       gs = client.getGroup(msg.to)
                       targets = []
                       for g in gs.members:
                           if _name in g.displayName:
                              targets.append(g.mid)
                       if targets == []:
                           sendMessage(msg.to,"Tidak Ada Member")
                           pass
                       else:
                           for target in targets:
                              try:
                                  client.kickoutFromGroup(msg.to,[target])
                                  print (msg.to,[g.mid])
                              except:
                                  sendMassage(msg.to,"Rata? Protect Anjeng")
                                  sendMassage(msg.to,"masih mauko sundala")
                if "Info" in msg.text:
                    nk0 = msg.text.replace("Info ","")
                    nk1 = nk0.lstrip()
                    nk2 = nk1.replace("@","")
                    nk3 = nk2.rstrip()
                    _name = nk3
                    gs = client.getGroup(msg.to)
                    targets = []
                    for s in gs.members:
                        if _name in s.displayName:
                            targets.append(s.mid)
                    if targets == []:
                        sendMessage(msg.to,"Tidak Ada Akun")
                        pass
                    else:
                        for target in targets:
                            try:
                                print (msg.to,"[displayName]:\n" + msg.contentMetadata["displayName"] + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu)) 
                            except:
                                sendMessage(msg.to,"Semoga Diterima disisinya")
                elif msg.text in ["Gurl"]:
                    if msg.toType == 2:
                        x = client.getGroup(msg.to)
                        if x.preventJoinByTicket == True:
                            x.preventJoinByTicket = False
                            client.updateGroup(x)
                        gurl = client.reissueGroupTicket(msg.to)
                        sendMessage(msg.to,"line://ti/g/" + gurl)
                    else:
                        if wait["lang"] == "JP":
                            sendMessage(msg.to,"Can't be used outside the group")
                        else:
                            sendMessage(msg.to,"Not for use less than group")
                elif "Mid @" in msg.text:
                    _name = msg.text.replace("Mid @","")
                    _nametarget = _name.rstrip(' ')
                    gs = client.getGroup(msg.to)
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            sendMessage(msg.to, g.mid)
                        else:
                            pass
                elif "Kick " in msg.text:
                    nk0 = msg.text.replace("Kick ","")
                    nk1 = nk0.lstrip()
                    nk2 = nk1.replace("@","")
                    nk3 = nk2.rstrip()
                    _name = nk3
                    gs = client.getGroup(msg.to)
                    targets = []
                    for s in gs.members:
                        if _name in s.displayName:
                            targets.append(s.mid)
                    if targets == []:
                        sendMessage(msg.to,"User Tidak Di Temukan")
                        pass
                    else:
                        for target in targets:
                            try:
                                client.kickoutFromGroup(msg.to,[target])
                                print (msg.to,[g.mid])
                            except:
                                sendMassage(msg.to,"Sundala")
                                sendMassage(msg.to,"Masih Mauko Bangsat!!!")
                elif "Invite " in msg.text:
                    midd = msg.text.replace("Invite ","")
                    client.findAndAddContactsByMid(midd)
                    client.inviteIntoGroup(msg.to,[midd])
                elif "Kick " in msg.text:
                    midd = msg.text.replace("Kick ","")
                    client.kickoutFromGroup(msg.to,[midd])
                elif ("Kick " in msg.text):
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    targets = []
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                       try:
                          client.kickoutFromGroup(msg.to,[target])
                       except:
                          pass
                elif "Bc:ct " in msg.text:
                    bctxt = msg.text.replace("Bc:ct ", "")
                    a = client.getAllContactIds()
                    for manusia in a:
                        sendMessage(manusia, (bctxt))
                elif "Bc:grup " in msg.text:
                    bctxt = msg.text.replace("Bc:grup ", "")
                    n = client.getGroupIdsJoined()
                    for manusia in n:
                        sendMessage(manusia, (bctxt))
                elif "Spam " in msg.text:
                   txt = msg.text.split(" ")
                   jmlh = int(txt[2])
                   teks = msg.text.replace("Spam "+str(txt[1])+" "+str(jmlh)+ " ","")
                   tulisan = jmlh * (teks+"\n")
                   if txt[1] == "on":
                        if jmlh <= 99999:
                             for x in range(jmlh):
                                    sendMessage(msg.to, teks)
                                    sendMessage(msg.to, teks)
                                    sendMessage(msg.to, teks)
                                    sendMessage(msg.to, teks)
                                    sendMessage(msg.to, teks)
                                    sendMessage(msg.to, teks)
                                    sendMessage(msg.to, teks)
                                    sendMessage(msg.to, teks)
                                    sendMessage(msg.to, teks)
                                    sendMessage(msg.to, teks)
                        else:
                               sendMessage(msg.to, "Melebihi Batas!!! ")
                   elif txt[1] == "off":
                         if jmlh <= 99999:
                               sendMessage(msg.to, tulisan)
                               sendMessage(msg.to, tulisan)
                               sendMessage(msg.to, tulisan)
                               sendMessage(msg.to, tulisan)
                               sendMessage(msg.to, tulisan)
                               sendMessage(msg.to, tulisan)
                               sendMessage(msg.to, tulisan)
                               sendMessage(msg.to, tulisan)
                               sendMessage(msg.to, tulisan)
                               sendMessage(msg.to, tulisan)
                         else:
                               sendMessage(msg.to, "Melebihi Batas!!! ")
                if msg.text == "Mid":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "Gid":
                    sendMessage(msg.to, msg.to)
                if "Gname:" in msg.text:
                    key = msg.text[22:]
                    group = client.getGroup(msg.to)
                    group.name = key
                    client.updateGroup(group)
                    sendMessage(msg.to,"Group Name"+key+"Canged to")
                if msg.text == "Url":
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
                if "join" in msg.text:
                    G = client.getGroup(msg.to)
                    ginfo = client.getGroup(msg.to)
                    G.preventJoinByTicket = False
                    client.updateGroup(G)
                    invsend = 0
                    Ticket = client.reissueGroupTicket(msg.to)
                    client.acceptGroupInvitationByTicket(msg.to,Ticket)
                if msg.text == "Link on":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "already open")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL Open")
                if msg.text == "Link off":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "already close")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL close")
                if msg.text == "Cancel":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "No one is inviting.")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + " Done")
                if "Invite:" in msg.text:
                    key = msg.text[-33:]
                    client.findAndAddContactsByMid(key)
                    client.inviteIntoGroup(msg.to, [key])
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+" I invited you")
                if msg.text == "Me":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    client.sendMessage(M)
                if "Show:" in msg.text:
                    key = msg.text[-33:]
                    sendMessage(msg.to, text=None, contentMetadata={'mid': key}, contentType=13)
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+"'s contact")
                if msg.text == "Gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                if msg.text == "Sider":
                    sendMessage(msg.to, "􀜁􀅔Har Har􏿿")
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        pass
                    wait['readPoint'][msg.to] = msg.id
                    wait['readMember'][msg.to] = ""
                    wait['setTime'][msg.to] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    wait['ROM'][msg.to] = {}
                    print wait
                if msg.text == "Show read":
                    if msg.to in wait['readPoint']:
                        if wait["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait["ROM"][msg.to].items():
                                print rom
                                chiya += rom[1] + "\n"

                        sendMessage(msg.to, "T E R C Y D U K %s\n􀜁􀅔Har Har􏿿\n\nT E R S A N G K A\n%s􀜁􀅔Har Har􏿿\n\nTanggal Dan Waktu Kejadian:\n[%s]"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        sendMessage(msg.to, "Ketik「Sider」􀜁􀅔Har Har􏿿")
                else:
                    pass
        else:
            pass

    except Exception as e:
        print e
        print ("\n\nSEND_MESSAGE\n\n")
        return

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:
    tracer.execute()
