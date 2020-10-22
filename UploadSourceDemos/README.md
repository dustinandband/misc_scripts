# SourceTVDemoUploader  

Edit of someone else's (https://github.com/volnt/e2e-upload/blob/07a29fe00345492193c137774948de8c3e5b5246/project/upload/backblaze.py)[script] for uploading sourceTV demo recordings to backblack b2 storage.  

Edits needed to Survival Network auto-restart.sh script:  

1)  

```
#Demo upload functionality:
demofiles_path=(
'/root/l4d2_server1/left4dead2/addons/sourcemod/data/SourceTVDemos'
'/root/l4d2_server2/left4dead2/addons/sourcemod/data/SourceTVDemos'
)
```  

changed to:  

```
#Demo upload functionality:

b2_authorize_account_id='' # use dustin's info
b2_authorize_accountkey=''

demofiles_path=(
'/root/l4d2_server1/left4dead2/addons/sourcemod/data/SourceTVDemos'
'/root/l4d2_server2/left4dead2/addons/sourcemod/data/SourceTVDemos'
)
```  

2)  

```
# Upload SourceTV demos to web server
echo "Uploading demo files to webserver..."
gzip ${demofiles_path[$j]}/*.dem 2>/dev/null
sshpass -p $webserver_pass rsync -avhiP -e ssh ${demofiles_path[$j]} $webserver_user@$webserver_host:$demoupload_destpath && \
rm ${demofiles_path[$j]}/* 2>/dev/null
```  

changed to:  

TODO