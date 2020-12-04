# SourceTVDemoUploader  

### Update: Dec 4, 2020  

Added some printed text to help debug why files aren't available for download at the survival archive website.  

1)  

Within the restart.sh script (previously auto-restart.sh), change this:  
```sh
./SourceTVDemoUploader.py ${demofiles_path[$j]} $b2_authorize_account_id $b2_authorize_accountkey
```  

to this:  
 
```sh
./SourceTVDemoUploader.py ${demofiles_path[$j]} $b2_authorize_account_id $b2_authorize_accountkey > SourceTVUploadLog.log 
```  

2)  
Download new SourceTVDemoUploader.py file (or just delete previous one and have restart.sh script download it again), which just prints out the json response of each sourceTV demo upload to a log file named SourceTVUploadLog.log.  

-------------------------------------------  

Edit of someone else's [script](https://github.com/volnt/e2e-upload/blob/07a29fe00345492193c137774948de8c3e5b5246/project/upload/backblaze.py) for uploading sourceTV demo recordings to backblack b2 storage.  

Edits needed to Survival Network auto-restart.sh script:  

1)  

``` sh
#Demo upload functionality:
demofiles_path=(
'/root/l4d2_server1/left4dead2/addons/sourcemod/data/SourceTVDemos'
'/root/l4d2_server2/left4dead2/addons/sourcemod/data/SourceTVDemos'
)
```  

changed to:  

``` sh
#Demo upload functionality:

b2_authorize_account_id='' # use dustin's info
b2_authorize_accountkey=''

demofiles_path=(
'/root/l4d2_server1/left4dead2/addons/sourcemod/data/SourceTVDemos'
'/root/l4d2_server2/left4dead2/addons/sourcemod/data/SourceTVDemos'
)
```  

2)  

``` sh
# Upload SourceTV demos to web server
echo "Uploading demo files to webserver..."
gzip ${demofiles_path[$j]}/*.dem 2>/dev/null
sshpass -p $webserver_pass rsync -avhiP -e ssh ${demofiles_path[$j]} $webserver_user@$webserver_host:$demoupload_destpath && \
rm ${demofiles_path[$j]}/* 2>/dev/null
```  

changed to:  

``` sh
# Upload SourceTV demos to backblaze b2
echo "Uploading demo files to backblaze b2..."
gzip ${demofiles_path[$j]}/*.dem 2>/dev/null

if [ ! -e "SourceTVDemoUploader.py" ]; then
	curl -o SourceTVDemoUploader.py 'https://raw.githubusercontent.com/dustinandband/misc_scripts/main/UploadSourceDemos/SourceTVDemoUploader.py'
	chmod +x SourceTVDemoUploader.py
fi

./SourceTVDemoUploader.py ${demofiles_path[$j]} $b2_authorize_account_id $b2_authorize_accountkey
```  