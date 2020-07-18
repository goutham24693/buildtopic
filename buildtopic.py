from pygerrit2 import GerritRestAPI, HTTPBasicAuth
import jenkins


topic = "topicname"


username = "username"
password = "passwd"
branch = "branch"
email = "gautham.durairaj@xxx.yy"


def jenkins_build(GERRIT_PATCH_SET):
	global branch
	global email
	jenkisurl = "https://jenkins.xxx.yyy.zz/jenkins/"
	job = "job"
	targetimage = "image"
	machine = "machine"
	repo = "ssh://gerrit.xxxxxxx.yyy:12345/aaa/bbbbb/cccccc/dddddddddddd"
	deploy = "abcdeploy@12.345.678.910"
	nexus = "https://xxxxxx.yyyyyyyyy.zzzzzzzzz.com/abc"

	server = jenkins.Jenkins(jenkisurl, username,
	                         password)
	params = { "BRANCH" : branch, "TARGET_IMAGE" : targetimage, "MACHINE" : machine,
	"PROJECT_REPO" : repo, "DEPLOY_IP" : deploy, "NEXUS_REPO" : nexus, "EMAIL" : email,
	"GERRIT_PATCH_SET" : GERRIT_PATCH_SET}
	print(server.build_job(job, params))


def prepare_patch_set(topic):
	gerrit_url = "https://gerrit.xxxxxxxx.com/"
	GERRIT_PATCH_SET = str()
	auth = HTTPBasicAuth(username, password)
	rest = GerritRestAPI(url=gerrit_url, auth=auth)
	#changes = rest.get("/changes/?q=owner:self%20status:open")
	changes = rest.get("/changes/?q=topic:" + topic)
	for change in changes:
		#if change["status"] != "NEW" or change["mergeable"] == False:
		if change["status"] != "NEW":
			print (change["subject"] + " " + change["project"] + " " + str(change["_number"]) + " is not mergeable or already merged")
			exit(1)
		else:
			#print (change["subject"] + " " + change["project"] + " " + str(change["_number"]))
			#info = rest.get("/changes/?q=change:%d&o=CURRENT_REVISION&o=CURRENT_REVISION&o=CURRENT_COMMIT&o=CURRENT_FILES" %change["_number"])
			changeId = change["_number"]
			info = rest.get("/changes/?q=change:%d&o=CURRENT_REVISION&o=CURRENT_COMMIT" %changeId)
			repo = change["project"]
			currefId = (info[0]["revisions"][info[0]["current_revision"]]["_number"])
			GERRIT_PATCH_SET = GERRIT_PATCH_SET + " | " + (repo + " " + str(change["_number"]) + "/" + str(currefId))
	return GERRIT_PATCH_SET


GERRIT_PATCH_SET = prepare_patch_set(topic)[3:]
print("building patch list " + GERRIT_PATCH_SET)
jenkins_build(GERRIT_PATCH_SET)
