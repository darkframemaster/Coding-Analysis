#git command
##git set
`git`                                                //查看是否有git可用                                    
`sudo apt-get install git  `    			//ubuntu安装git 	                                                                     
`git --version`		                      // git版本	    			
`git config --global user.name "yourname"`	//yourname是你的名字                                       
`git config --global user.email "email@example.com"`	//email@example.com是你的邮箱                                                                                                                                                                                                       
`git config --global color.ui true`//在git命令输出中开启颜色显示         

                                                                                          
##git useful
`git init`//初始化当前文件夹为git工作区                                                 
`git init filename`//初始化一个叫filename的工作区在当前文件夹下		**init操作会在工作区中会生成一个叫.git的文件夹 我们称之为git版本库**                      
`git add filename`	//添加文件到咱存区 可反复使用添加多个文件                                                                                                                                                                                                                                                                                                                           
`git commit -m "changes"`	//添加改动说明 "changes"为本次添加的改动 建议每次都写     **只有在完成git add以及git commit之后才算真真完成改动,每一个commit操作都非常非常的重要**                                                                                                                                                                                                                          
`git status`		//仓库当前的状况，文件的修改情况                                             
`git diff filename` 	//查看文件的改动内容                                                    
`git checkout -- filename`//撤销工作区的修改 **--后面有一个空格**                                                                                                                                                                                                                                       
`git reset HEAD filename`//撤销暂存区的修改，完了之后还得撤销工作区的修改才能彻底退回                                                                                                                                                                            
`git reset --hard commit_id`	//让文件回到commit_id的版本，撤销操作的终极操作                                                                                                                                                                                                                                              
`git log`			//查看文件的历史版本 以及commit_id                                 
`git log --pretty=oneline`//                                                                                                        
`git log --graph --pretty=oneline --abbrev-commit`//                                                
`git reflog`		//查看文件的历史版本 比较强大                                                                         
`git rm filename` //从版本库中删除文件filename，记得git commit
`git checkout -- filename` //文件删错拉。。。用git checkout搞定**git checkout其实是用版本库里的版本替换工作区的版本无论是修改还是删除都可以一键还原**

##git and github
>*github我们的远程仓库* 
                                                                                                                                                                                               
注册github什么的我就不说了。直接进入ssh密钥设置。你的本地git仓库和github仓库之间的传输是通过ssh加密的，所以，需要一点设置：                                                                                                         
1. 创建SSH Key。在用户**主目录**下，看看有没有.ssh目录，如果有，再看看这个目录下有没有id_rsa和id_rsa.pub这两个文件，如果已经有了，可直接跳到下一步。如果没有，打开Shell（Windows下打开Git Bash），创建SSH Key：                                                                                                                                                                          
`$ssh -keygen -t rsa -C "youremail@example.com"`                                                                                                        
2. 登陆GitHub，打开“Account settings”，“SSH Keys”页面：然后，点“Add SSH Key”，填上任意Title，在Key文本框里粘贴**id_rsa.pub**文件的内容                                                                                                                             
**出现ssh: connect to host github.com port 22: Connection refused请参考**[darkframexue](http://www.jianshu.com/writer#/notebooks/1141614/notes/1513755/preview)

###git push and clone
>从本地到远程库

在github上创建一个叫作*repository*的仓库,打开终端执行下列操作.
`cd /path/to/your/workspace`//进入本地仓库                                                                                                                                                                                                                                                                                                                   
`git remote add origin git@github.com:yourname/repositoryname.git`//进行本地仓库与远程仓库的关联
**yourname是你的用户名，repositoryname是你的远程仓库的名字。**                                                       
`git remote add gitcaffe@gitcaffe.com:yourname/repositoryname.git`//当然可以选择中国的git caffe                 
`git push -u origin master`//**origin is name of the github**                                                                                                                                                                                                                     
`git push -u gitcafe master`//**push to git caffe** gitcafe                                                                                                                                                           
`git push origin master`//**only the first push need -u**                                                                                                                                                             
>从远程库到本地     
                                                                                                                                                                                                                   
create a new repository name as "whateveryoulike"**whateveryoulike is the repository name**                                                                                                                             
and you can choose *Initialize this repository with a README* to add a README.md file **README.md ask you use markdown to write in** [helpfor_markdown](www.baidu.com)                                                                             
`git clone git@github.com:yourname/repositoryname.git`//clone a repository in your computer                                                                                                                                     
                                                                                                                                                                             
##git branch
`git branch`//show the branches                                                                                                                                     
`git branch branchname`//create a new branch                                                                                                                                                                        
`git checkout branchname`//move to the branch named as branchname                                                                                                                       
`git checkout -b branchname`//create a new branch and move to it                                                                                                                                                
`git merge branchname`//合并branchname分支到**当前分支上（master）**                                                                                                                        
`git branch -d branchname`//delete the branch named as branchname                                                                                                                                                                   

通常，合并分支时，如果可能，git会用fast forward模式，但在这种模式下，删除分支后，会丢掉分支信息。如果要强制禁用fast forward模式，git就会在**（merge）合并**时生成一个新的**commit**，这样，从分支历史上就能看出分支信息。                                                                           
>用--no-ff方式的gitmerge：

`git merge --no-ff -m “merge with no-ff” branchname`//`--no-ff` forbit fast *Forward* `-m` include commit

##git  bug
`git stash//把当前工作现场“储存”起来。

`git checkout wherebugis`//切换到bug所在分支

`git checkout -b Fixbug-101`//创建一个bug修复分区，切换到该分区

。。。//修复bug

`git add bugfile`

`git commit -m “fix bug 101”

`git checkout master`//修复完成后回到master分区

`git merge --no-ff -m “merge bug fix 101” Fixbug-101`//合并分区

`git branch -d Fixbug-101`//删除分区

`git checkout dev`//回到dev分区接着。。。

`git status`//看看刚才的stash是否成功啦，并没有发现有什么修改，难道没有保存？

`git stash list`//查看stash的列表，工作现场还在只是被git存到什么地方去了，需要恢复一下

`git stash pop`//回复的同时把stash的内容删除

`git stash list`//好了什么也没有了

`git stash apply`//恢复而不清除stash

`git stash drop`//配合`git stash apply`使用，删除stash

如果有多次stash，恢复的时候，先用`git stash list`查看，然后恢复指定的文件：

`git stash apply stash@{0}`//恢复指定的stash对象
                                                                                                                                                                                                                                                                                                   
##git for us
###push
`git remote`//查看远程库的信息

`git remote -v`//显示更详细的信息

`git push origin branch_name`//推送时，要指定本地分支，这样，Git就会把该分支推送到远程库对应的远程分支上.

但是，并不是一定要把本地分支往远程推送，那么，哪些分支需要推送，哪些不需要呢？

* master分支是主分支，因此要时刻与远程同步；

* dev分支是开发分支，团队所有成员都需要在上面工作，所以也需要与远程同步；

* bug分支只用于在本地修复bug，就没必要推到远程了，除非老板要看看你每周到底修复了几个bug；

* feature分支是否推到远程，取决于你是否和你的小伙伴合作在上面开发。

###catch
现在以**你的小伙伴**的身份从远程库clone：记得添加他的SSH密钥到你的git。

`git clone git@github.com:darkframexue/learngit`

`git branch`//当你的小伙伴从远程库clone时，默认情况下，你的小伙伴只能看到本地的master分支。                                                                                                                                                                                                                                                                                                   

`git checkout -b dev origin/dev`//创建远程origin的dev分支到本地

`git add filename`

`git commit -m "information"`

`git push origin dev`

//你的小伙伴已经向origin/dev分支推送了他的提交，而碰巧**你**也对同样的文件作了修改，并试图推送：
`git add filename`

`git commit -m "information"`

`git push origin dev`//推送失败,推送的提交有冲突，解决办法也很简单，Git已经提示我们，先用git pull把最新的提交从origin/dev抓下来，然后，在本地合并，解决冲突，再推送：

`git pull`//也失败了，原因是没有指定本地dev分支与远程origin/dev分支的链接，根据提示，设置dev和origin/dev的链接.

`git branch --set-upstream dev origin/dev`//设置dev和origin/dev的链接.

`git pull`//OK

####多人协作的工作模式通常是这样：

1.    首先，可以试图用git push origin branch-name推送自己的修改；

2.    如果推送失败，则因为远程分支比你的本地更新，需要先用git pull试图合并；

3.    如果合并有冲突，则解决冲突，并在本地提交；

4.    没有冲突或者解决掉冲突后，再用git push origin branch-name推送就能成功！

如果git pull提示“no tracking information”，则说明本地分支和远程分支的链接关系没有创建，用命令git branch --set-upstream branch-name origin/branch-name。


##标签
###创建标签
创建标签--git的版本名牌
`git branch`

`git checkout branch_name`//切换到需要打标签的分支上

`git tag v1.0`//敲命令git tag <name>就可以打一个新标签,**默认标签是打在最新提交的commit上的。**

`git tag v1.1 commit_id`//在对应的commit_id处贴上标签。

`git tag -a v1.2 -m "vertion 1.2 released" commit_id`创建带有说明的标签，用-a指定标签名，-m指定说明文字.

`git tag -s v1.3 -m "signed version 1.3 released" commit_id`//通过-s用私钥签名一个标签

`git tag`//查看所有标签

**注意**，标签不是按时间顺序列出，而是按字母排序的。可以用git show <tagname>查看标签信息
`git show v1.0`//查看标签信息

###操作标签
因为创建的标签都只存储在本地，不会自动推送到远程。所以，打错的标签可以在本地安全删除。
`git tag -d v1.0`//标签打错了，也可以删除

`git push origin v1.0`//推送某个标签到远程

`git push origin --tag`//一次性推送全部尚未推送到远程的本地标签

要删除远程标签就麻烦一点，先从本地删除
`git tag -d v1.0`

`git push origin:refs/tags/v1.0`//从远程删除。删除命令也是push.

##git grep
`git grep` 			//查看文件内容                                                                                                                                                      
`git grep` "工作区文件内容搜索"	//文件内容搜索                                                                                                       

##git config
`git config --global color.ui true`//让Git显示颜色，会让命令输出看起来更醒目
`git config -e`			//打开.git/config文件进行编辑，在工作区下执行该命令                                                                      
`git config -e --global`		//打开/home/xuehao/.gitconfig(用户主目录下的.gitconfig文件)全局配置文件进行编辑。                                                                                                                                                                                                                                   
`git config -e --system`		//打开/etc/gitconfig系统级配置文件进行比编辑，如果Git安装在非标准位置，则这个系统级的配置文件也可能是在另外的位置。                                                                                                                                                                           
**版本库级别的配置文件的优先级最高，全局配置文件次之，系统级配置文件优先级最低。git配置文件都是INI文件格式。**                                                                                        
`git config core.dare`		//查看ini文件中care小节的dare值                                                                                              
`git config a.b something`//设置ini文件下的a小节的b值为something                                                       
`git config x.y.z others`		//[x "y"]小节的z值为others                                    
`GIT_CONFIG=test.ini git config a.b.c.d "hello world"	`//向配置文件test.ini中添加配置                                                     

`git config user.name`		//显示用户名                                                                                                                   
`git config user.email`		//显示用户邮箱                                                                                             
`git config --unset --global user.name	`//删除用户名                                                                   
`git config --unset --global user.email`	//删除用户邮箱                                                                                 
                                            
##git别名设置
*所有用户都能使用别名*                                                                                                                                
`sudo git config --system alias.st status`                                                                                                                     
`sudo git config --system alias.ci commit`                                                                                                                                                                    
`sudo git config --system alias.co checkout`
`sudo git config --system alias.br branch`                                                                      
*只在本用户的全局配置中使用别名*                                                                                           
`git config --global alias.st status`                                                                                       
`git config --global alias.ci commit`                                                                                                                       
`git config --global alias.co checkout`                                                                                             
`git config --global alias.br branch`         
###不常用的                                                                                                                      
`strace -e 'trace=file' git *`	//跟踪这条git命令的磁盘访问。                                                                                  
`git rev-parse --git-dir`		//显示版本库.git目录所在的位置                                                                 
`git rev-parse --show-toplevel`   //显示工作区的根目录                                                                                         
`git rev-parse --show-cdup`	//显示从当前目录（cd）后退（up）到工作区的根的深度。                                                                     
