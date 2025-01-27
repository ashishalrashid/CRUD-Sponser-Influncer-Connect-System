from flask import Flask, render_template, url_for ,request , redirect ,flash ,send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from sqlalchemy import text , UniqueConstraint
from dateutil.relativedelta import relativedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

app=Flask(__name__)
app.secret_key='85078db50ab69cef25ec3599a7013425a6e01ba53cbf685b'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
app.config['UPLOAD_FOLDER'] = 'static/images'
db =SQLAlchemy(app)

class Sponser(db.Model):
    sid=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(),nullable=False)
    password=db.Column(db.String(),nullable=False)
    budget=db.Column(db.Integer,nullable=False )
    flag=db.Column(db.Integer,nullable=False,default=0 ) #can be 0, 1 , 2 

class Influncer(db.Model):
    iid=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(),nullable=False)
    password=db.Column(db.String(),nullable=False)
    follower=db.Column(db.Integer,nullable=False )
    Niche=db.Column(db.String(),nullable=False)  #tech ,gaming,beauty,fitness,travel,food,education,lifestyle,misc
    flag=db.Column(db.Integer,nullable=False,default=0 )

class Admin(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(),nullable=False)
    password=db.Column(db.String(),nullable=False)

class Campaign(db.Model):
    cid=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(),nullable=False)
    sponser_id=db.Column(db.Integer,db.ForeignKey('sponser.sid'),nullable=False)
    Description=db.Column(db.String())
    visibilty=db.Column(db.Integer,default=0) #0-public #1-private
    start_date=db.Column(db.DateTime)
    end_date=db.Column(db.DateTime)

class ad_request(db.Model):
    adid=db.Column(db.Integer, primary_key=True)
    campaign_id=db.Column(db.Integer,db.ForeignKey('campaign.cid'),nullable=False)
    influncer_id=db.Column(db.Integer,db.ForeignKey('influncer.iid'),nullable=False)
    message=db.Column(db.String())
    requirments=db.Column(db.String())
    payment=db.Column(db.Integer)
    status=db.Column(db.String())  #(waitfor_inf ,waitfor_sp , Accepted,negotiate_from_inf , negotiate_ form , Rejected)
    __table_args__ = (
        UniqueConstraint('campaign_id', 'influncer_id', name='unique_campaign_influencer'),
    )


@app.route('/',methods=['POST','GET'])
def chooselogin():
    if request.method=='POST':
        choice=request.form['logch']  #Sponser , Inf ,Admin
        uname=request.form['username']
        upass=request.form['password']
        print(choice,uname,upass)

        if choice == "Sponser":
            query = text("""SELECT sid, password
                        FROM Sponser
                    WHERE name = :uname""")
            try:
                result = db.session.execute(query, {'uname': uname})
                credentials = result.fetchall()
                if credentials and upass == credentials[0][1]:
                    sid = credentials[0][0]
                    return redirect(f'sponserdash/{sid}')
            except Exception as e:
                print(f"Error: {e}")
            msg = "Invalid login"
            return render_template('chooselogin.html', msg=msg)

        if choice == "Inf":
            query = text("""SELECT iid, password
                            FROM Influncer
                            WHERE name = :uname""")
            try:
                result = db.session.execute(query, {'uname': uname})
                credentials = result.fetchall()
                if credentials and upass == credentials[0][1]:
                    iid = credentials[0][0]
                    return redirect(f'infdash/{iid}')
            except Exception as e:
                print(f"Error: {e}")
                msg = "Invalid login"
                return render_template('chooselogin.html', msg=msg)

        if choice == "Admin":
            query = text("""SELECT id, password
                        FROM admin
                        WHERE name = :uname""")
            try:
                result = db.session.execute(query, {'uname': uname})
                credentials = result.fetchall()
                if credentials and upass == credentials[0][1]:
                    aid = credentials[0][0]
                    return redirect(f'admindash/{aid}')
            except Exception as e:
                print(f"Error: {e}")
                msg = "Invalid login"
                return render_template('chooselogin.html', msg=msg)
    return render_template("chooselogin.html")

@app.route('/createsp',methods=['POST','GET'])
def createsp():
    if request.method=='POST':
        ucreate=request.form['username']
        pcreate=request.form['password']
        budget=request.form['budget']
        newuser=Sponser(name=ucreate,password=pcreate,budget=budget)

        try:
            db.session.add(newuser)
            db.session.commit()
            return redirect('/')
        except:
            return "error in creating"
    else:
        return render_template('createsp.html')

@app.route('/createinf',methods=['POST','GET'])
def createinf():
    if request.method=='POST':
        ucreate=request.form['username']
        pcreate=request.form['password']
        followers=request.form['follower']
        newuser=Influncer(name=ucreate,password=pcreate,follower=followers)

        try:
            db.session.add(newuser)
            db.session.commit()
            return redirect('/')
        except:
            return "error in creating"
    else:
        return render_template('createinf.html')

@app.route('/sponserdash/<int:sid>')
def sponserdash(sid):
    query=text("""SELECT cid,name , end_date
                from Campaign
                where sponser_id=:sid""")
    
    result=db.session.execute(query,{'sid':sid})
    camp_list=result.fetchall()
    return render_template('sponserdash.html',camp_list=camp_list,sid=sid)

@app.route('/createcamp/<int:sid>',methods=['POST','GET'])
def createcamp(sid):
    if request.method=='POST':
        cname=request.form['camp_name']
        desc=request.form['camp_desc']
        duration= int(request.form['duration'])
        curr_date =datetime.now()
        fenddate = curr_date + relativedelta(months=duration)
        newcamp=Campaign(name=cname,Description=desc,start_date=curr_date,end_date=fenddate,sponser_id=sid)

        try:
            db.session.add(newcamp)
            db.session.commit()
            return redirect(f'/sponserdash/{sid}')
        except:
            return "error in creating"
    else:
        return render_template('createcamp.html',sid=sid)

@app.route('/camppage/<int:sid>/<int:cid>')
def camppage(sid,cid):
    query=text("""select *
                from campaign 
                where cid=:cid""")
    result=db.session.execute(query,{'cid':cid})
    camp_info=result.fetchall()

    query1=text("""Select i.name , i.follower , a.status , i.iid
                from influncer as i
                join ad_request as a on a.influncer_id=i.iid
                where a.campaign_id=:cid""")
    result1=db.session.execute(query1,{'cid':cid})
    inf_members=result1.fetchall()
    return render_template('camppage.html',sid=sid,cid=cid,camp_info=camp_info,inf_members=inf_members)

# delcamp/{{sid}}/{{cid}}"
@app.route('/delcamp/<int:sid>/<int:cid>')
def delcamp(sid,cid):
    query=text("""delete from campaign
                where cid=:cid""")
    query1=text("""delete from ad_request
                where campaign_id=:cid""")
    db.session.execute(query,{'cid':cid})
    db.session.execute(query1,{'cid':cid})
    db.session.commit()
    return redirect(f'/sponserdash/{sid}')

@app.route('/editcamp/<int:sid>/<int:cid>',methods=['POST','GET'])
def editcamp(sid,cid):
    if request.method=='POST':
        cname=request.form['camp_name']
        desc=request.form['camp_desc']
        query=text("""update campaign
                    set name=:cname,
                    description=:desc
                    where cid=:cid""")
        db.session.execute(query,{'cid':cid,'cname':cname,'desc':desc})
        db.session.commit()
        return redirect(f'/camppage/{sid}/{cid}')
    else:
        return render_template('editcamp.html',sid=sid,cid=cid)

@app.route('/makecamppublic/<int:sid>/<int:cid>',methods=['POST','GET'])
def makecamppublic(sid,cid):
    query=text("""update campaign
                set visibilty=0
                where cid=:cid""")
    db.session.execute(query,{'cid':cid})
    db.session.commit()
    return redirect(f'/camppage/{sid}/{cid}')

@app.route('/makecampprivate/<int:sid>/<int:cid>',methods=['POST','GET'])
def makecampprivate(sid,cid):
    query=text("""update campaign
                set visibilty=1
                where cid=:cid""")
    db.session.execute(query,{'cid':cid})
    db.session.commit()
    return redirect(f'/camppage/{sid}/{cid}')

@app.route('/influncersearch/<int:sid>/<int:cid>',methods=['POST','GET'])
def influncersearch(sid,cid):
    if request.method=='POST':
        filter_name=request.form.get('search-inf','')
        search_by=request.form['num']
        # print(search_by)
        if filter_name and search_by=="Name":
            query=text("""Select * from influncer where name like :filter_name""")
            result=db.session.execute(query,{'filter_name':f'%{filter_name}%'})
            all_inf=result.fetchall()
            # print(all_inf)
            return render_template('influncersearch.html',all_inf=all_inf,cid=cid,sid=sid)
        
        if filter_name and search_by=="niche":
            query=text("""Select * from influncer where niche like :filter_name""")
            result=db.session.execute(query,{'filter_name':f'%{filter_name}%'})
            all_inf=result.fetchall()
            # print(all_inf)
            return render_template('influncersearch.html',all_inf=all_inf,cid=cid,sid=sid)

    query=text("""Select * from influncer""")
    result=db.session.execute(query)
    all_inf=result.fetchall()
    return render_template('influncersearch.html',all_inf=all_inf,sid=sid,cid=cid)

@app.route('/infpage/<int:sid>/<int:cid>/<int:iid>',methods=['POST','GET'])
def infpage(sid,cid,iid):
    if request.method=="POST":
        meg=request.form.get('message','')
        reqm=request.form.get('Requirments','')
        pay=request.form.get('payment','')
        newad=ad_request(campaign_id=cid,influncer_id=iid,message=meg,requirments=reqm,payment=pay,status="waitfor_inf")
        db.session.add(newad)
        db.session.commit()
        
    query=text("""select  *
                from Influncer
                where iid=:iid""")
    query1=text("""select * from ad_request where campaign_id=:cid and influncer_id=:iid""")
    result=db.session.execute(query,{'iid':iid})
    result1=db.session.execute(query1,{'iid':iid,'cid':cid})
    ad_info=result1.fetchone()
    inf_info=result.fetchone()
    print(ad_info)
    if ad_info:
        ad_info=ad_info
    else:
        ad_info="gg"
    return render_template('infpage.html',inf_info=inf_info,sid=sid,cid=cid,iid=iid,ad_info=ad_info)

@app.route('/reportinf/<int:sid>/<int:cid>/<int:iid>')
def reportinf(sid,cid,iid):
    query=text("""update influncer
                set flag=1
                where iid=:iid""")
    db.session.execute(query,{'iid':iid})
    db.session.commit()
    flash('reported')
    return redirect(f'/infpage/{sid}/{cid}/{iid}')

@app.route('/approveadreq/<int:sid>/<int:cid>/<int:iid>')
def approveadreq(sid,cid,iid):
    query=text("""Update ad_request
                set status="Approved"
                where campaign_id=:cid and Influncer_id=:iid""")
    db.session.execute(query,{'cid':cid,'iid':iid})
    db.session.commit()
    return redirect(f'/infpage/{sid}/{cid}/{iid}')

@app.route('/dropinf/<int:sid>/<int:cid>/<int:iid>')
def dropinf(sid,cid,iid):
    query=text("""Update ad_request
                set status="Rejected"
                where campaign_id=:cid and Influncer_id=:iid""")
    db.session.execute(query,{'cid':cid,'iid':iid})
    db.session.commit()
    return redirect(f'/infpage/{sid}/{cid}/{iid}')

@app.route('/negotiate/<int:sid>/<int:cid>/<int:iid>',methods=['POST','GET'])
def negotiate(sid,cid,iid):
    if request.method=="POST":
        new_pay=request.form['new_pay']
        query=text("""update ad_request
                    set status="negotiate_from_sponser",
                    payment =:new_pay
                    where campaign_id=:cid and influncer_id=:iid
                    """)
        db.session.execute(query,{'new_pay':new_pay,'cid':cid,'iid':iid})
        db.session.commit()
        return redirect(f'/infpage/{sid}/{cid}/{iid}')
    return render_template('negotiate.html',sid=sid,cid=cid,iid=iid)

@app.route('/searchbyrange/<int:sid>/<int:cid>',methods=['POST','GET'])
def searchbyrange(sid,cid):
    if request.method=="POST":
        lrange=request.form.get('lrange','')
        hrange=request.form.get('hrange','')
        if lrange=='':
            lrange=0
        if hrange=='':
            hrange=100000000
        query=text("""select * from influncer
                    where follower between :lrange and :hrange""")
        result=db.session.execute(query,{'lrange':lrange,'hrange':hrange})
        all_inf=result.fetchall()
        return render_template('influncersearch.html',all_inf=all_inf,sid=sid,cid=cid)
    return render_template('searchbyrange.html',sid=sid,cid=cid)


@app.route('/infdash/<int:iid>')
def infdash(iid):
    query=text("""SELECT c.cid, c.name, s.name, a.status, a.payment
                FROM ad_request AS a
                JOIN campaign AS c ON c.cid = a.campaign_id
                JOIN sponser AS s ON s.sid = c.sponser_id
                WHERE a.influncer_id = :iid""")
    
    result=db.session.execute(query,{'iid':iid})
    ad_list=result.fetchall()
    print(ad_list)
    return render_template('infdash.html',ad_list=ad_list,iid=iid)

@app.route('/searchcamp/<int:iid>/',methods=['POST','GET'])
def searchcamps(iid):
    if request.method=='POST':
        filter_name=request.form.get('search-camp','')
        search_by=request.form['num']
        # print(search_by)
        if filter_name and search_by=="Name":
            query=text("""Select * from campaign where name like :filter_name and visibilty=0""")
            result=db.session.execute(query,{'filter_name':f'%{filter_name}%'})
            all_camp=result.fetchall()
            # print(all_inf)
            return render_template('searchcamp.html',all_camp=all_camp,iid=iid)
        
        if filter_name and search_by=="Sponser":
            query=text("""Select * from campaign as c
                        join sponsor as s on s.sid=c.sponser_id
                        where s.name like :filter_name and visibilty=0""")
            result=db.session.execute(query,{'filter_name':f'%{filter_name}%'})
            all_camp=result.fetchall()
            # print(all_inf)
            return render_template('searchcamp.html',all_camp=all_camp,iid=iid)

    query=text("""Select * from campaign where visibilty=0""")
    result=db.session.execute(query)
    all_camp=result.fetchall()
    return render_template('searchcamp.html',all_camp=all_camp,iid=iid)

@app.route('/searchbybudget/<int:iid>',methods=['POST','GET'])
def searchbybudget(iid):
    if request.method=="POST":
        lrange=request.form.get('lrange','')
        hrange=request.form.get('hrange','')
        if lrange=='':
            lrange=0
        if hrange=='':
            hrange=100000000
        query=text("""select * from campaign as c
                    join sponser as s on s.sid=c.sponser_id
                    where c.visibilty=0 
                    and s.budget between :lrange and :hrange """)
        result=db.session.execute(query,{'lrange':lrange,'hrange':hrange})
        all_camp=result.fetchall()
        return render_template('searchcamp.html',all_camp=all_camp,iid=iid)
    return render_template('searchbybudget.html',iid=iid)

@app.route('/campview/<int:iid>/<int:cid>',methods=['POST','GET'])
def campview(iid,cid):
    if request.method=="POST":
        meg=request.form.get('message','')
        reqm=request.form.get('Requirments','')
        pay=request.form.get('payment','')
        newad=ad_request(campaign_id=cid,influncer_id=iid,message=meg,requirments=reqm,payment=pay,status="waitfor_sp")
        db.session.add(newad)
        db.session.commit()
        
    query=text("""select  s.name,c.cid, c.name, c.description , c.start_date ,c.end_date ,s.flag
                from campaign as c
                join sponser as s on c.sponser_id=s.sid
                where c.cid=:cid""")
    
    query1=text("""select * from ad_request where campaign_id=:cid and influncer_id=:iid""")

    result=db.session.execute(query,{'cid':cid})
    camp_info=result.fetchone()

    result1=db.session.execute(query1,{'iid':iid,'cid':cid})
    ad_info=result1.fetchone()
    
    print(ad_info)
    if ad_info:
        ad_info=ad_info
    else:
        ad_info="gg"
    return render_template('campview.html',camp_info=camp_info,iid=iid,cid=cid,ad_info=ad_info)

@app.route('/reportcamp/<int:iid>/<int:cid>')
def reportcamp(iid,cid):
    query=text("""UPDATE sponser
                SET flag = 1
                WHERE sid IN (
                SELECT s.sid
                FROM sponser s
                JOIN campaign c ON c.sponser_id = s.sid
                WHERE c.cid = :cid)""")
    db.session.execute(query,{'cid':cid})
    db.session.commit()
    flash('reported','info')
    return redirect(f'/campview/{iid}/{cid}')

@app.route('/infapproveadreq/<int:iid>/<int:cid>')
def infapproveadreq(iid,cid):
    query=text("""Update ad_request
                set status="Approved"
                where campaign_id=:cid and Influncer_id=:iid""")
    db.session.execute(query,{'cid':cid,'iid':iid})
    db.session.commit()
    return redirect(f'/campview/{iid}/{cid}')

@app.route('/infnegotiate/<int:iid>/<int:cid>',methods=['POST','GET'])
def infnegotiate(iid,cid):
    if request.method=="POST":
        new_pay=request.form['new_pay']
        query=text("""update ad_request
                    set status="negotiate_from_inf",
                    payment =:new_pay
                    where campaign_id=:cid and influncer_id=:iid
                    """)
        try:
            db.execute(query, {'new_pay': new_pay, 'cid': cid, 'iid': iid})
            db.commit()
            return redirect(f'/campview/{iid}/{cid}')
        except:
            db.rollback()

            flash('Unique constraint error','error')
            return render_template('infnegotiate.html', cid=cid, iid=iid)
    return render_template('infnegotiate.html', cid=cid, iid=iid)

@app.route('/dropsp/<int:iid>/<int:cid>')
def dropsp(iid,cid):
    query=text("""Update ad_request
                set status="Rejected"
                where campaign_id=:cid and Influncer_id=:iid""")
    db.session.execute(query,{'cid':cid,'iid':iid})
    db.session.commit()
    return redirect(f'/campview/{iid}/{cid}')

@app.route('/admindash/<int:aid>/')
def admindash(aid):
    return render_template('admindash.html',aid=aid)

@app.route('/viewsp/<int:aid>/')
def viewsp(aid):
    query=text("""Select * from sponser""")
    result=db.session.execute(query)
    sp_all=result.fetchall()
    return render_template("viewsp.html",aid=aid,sp_all=sp_all)

@app.route('/viewinf/<int:aid>/')
def viewinf(aid):
    query=text("""Select * from influncer""")
    result=db.session.execute(query)
    inf_all=result.fetchall()
    return render_template('viewinf.html',aid=aid,inf_all=inf_all)

@app.route('/viewads/<int:aid>/')
def viewad(aid):
    query=text("""Select a.adid , c.name ,i.name ,a.status, a.payment
                from ad_request as a
                join influncer as i on a.influncer_id=i.iid
                join campaign as c on a.campaign_id=c.cid""")
    result=db.session.execute(query)
    ads_all=result.fetchall()
    return render_template('viewads.html',aid=aid,ads_all=ads_all)

@app.route('/viewcamp/<int:aid>/')
def viewcamp(aid):
    query=text("""Select c.cid , c.name,s.name,c.visibilty ,s.flag
                from campaign as c
                join sponser as s on s.sid=c.sponser_id""")
    result=db.session.execute(query)
    camp_all=result.fetchall()
    return render_template('viewcamp.html',aid=aid,camp_all=camp_all)

@app.route('/deletesp/<int:aid>/<int:sid>')
def deletesp(aid,sid):
    query=text("""delete from sponser
                where sid=:sid""")
    query1=text("""delete from campaign
                where sponser_id=:sid""")
    db.session.execute(query,{'sid':sid})
    db.session.execute(query1,{'sid':sid})
    db.session.commit()
    return redirect(f'/viewsp/{aid}')

@app.route('/deleteinf/<int:aid>/<int:iid>')
def deleteinf(aid,iid):
    query=text("""delete from influncer
                where iid=:iid""")
    query1=text("""delete from ad_request
                where influncer_id=:iid""")
    db.session.execute(query,{'iid':iid})
    db.session.execute(query1,{'iid':iid})
    db.session.commit()
    return redirect(f'/viewinf/{aid}')

@app.route('/deletead/<int:aid>/<int:adid>')
def deletead(aid,adid):
    query=text("""delete from ad_request
                where adid=:adid""")
    db.session.execute(query,{'adid':adid})
    db.session.commit()
    return redirect(f'/viewads/{aid}')

@app.route('/deletecamp/<int:aid>/<int:cid>')
def deletecamp(aid,cid):
    query=text("""delete from campaign
                where cid=:cid""")
    query1=text("""delete from ad_request
                where campaign_id=:cid""")
    db.session.execute(query,{'cid':cid})
    db.session.execute(query1,{'cid':cid})
    db.session.commit()
    return redirect(f'/viewcamp/{aid}')

@app.route('/spstat/<int:aid>')
def sps(aid):
    query = text("""select budget from sponser""")
    result = db.session.execute(query)
    sp_list = [row[0] for row in result.fetchall()]

    #plot
    df = pd.DataFrame(sp_list, columns=['budget'])
    fig, ax = plt.subplots()
    bins = range(0, int(df['budget'].max()) + 1000, 1000)  # Define bins with a size of 1000
    ax.hist(df['budget'], bins=bins, edgecolor='black')
    ax.set_title('Histogram of Sponsor Budgets')
    ax.set_xlabel('Budget')
    ax.set_ylabel('Number of Sponsors')

    img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'density_plot.png')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    plt.savefig(img_path)
    plt.close(fig)

    #calculate stats
    total_sps=len(sp_list)
    query1=text("""select max(budget) , min(budget),avg(budget)
            from sponser""")
    result1=db.session.execute(query1)
    min_max_sp=result1.fetchall()
    print(min_max_sp[0])
    query2=text("""select count(*) as camp_count
                from campaign
                group by sponser_id
                order by camp_count desc""")
    result2=db.session.execute(query2)
    grp_sp=result2.fetchall()
    maxcps=grp_sp[0][0]
    c_sum=0
    for s in grp_sp:
        c_sum=+s[0]
    avgcps=c_sum/len(grp_sp)

    return render_template('spstats.html', img_filename='density_plot.png',aid=aid,total_sps=total_sps,min_max_sp=min_max_sp,maxcps=maxcps, avgcps=avgcps)

@app.route('/infstats/<int:aid>')
def infstat(aid):
    query = text("""select follower from influncer""")
    result = db.session.execute(query)
    inf_list = [row[0] for row in result.fetchall()]

    #plot
    df = pd.DataFrame(inf_list, columns=['follower'])
    fig, ax = plt.subplots()
    bins = range(0, int(df['follower'].max()) + 1000, 1000)  # Define bins with a size of 1000
    ax.hist(df['follower'], bins=bins, edgecolor='black')
    ax.set_title('Histogram of Influncer reach')
    ax.set_xlabel('Followers or Subscribers')
    ax.set_ylabel('Number of Influncers')

    img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'density_plot1.png')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    plt.savefig(img_path)
    plt.close(fig)

    #calculate stats
    total_inf=len(inf_list)
    query1=text("""select max(follower) , min(follower),avg(follower)
            from influncer""")
    result1=db.session.execute(query1)
    min_max_inf=result1.fetchall()
    query2=text("""select count(*) as ad_count
                from ad_request
                group by influncer_id
                order by ad_count desc""")
    result2=db.session.execute(query2)
    grp_inf=result2.fetchall()
    maxipa=grp_inf[0][0]
    print(grp_inf)
    a_sum=0
    for i in grp_inf:
        a_sum=+i[0]
    avgipa=a_sum/len(grp_inf)
    avgipa=round(avgipa,2)

    return render_template('infstats.html', img_filename='density_plot1.png',aid=aid,total_inf=total_inf,min_max_inf=min_max_inf,maxipa=maxipa,avgipa=avgipa)

            # <a href="/ignorespflag/{{aid}}/{{sp[4]}}">Dismiss</a>
            # <a href="/flagspflag/{{aid}}/{{sp[4]}}

@app.route('/ignorespflag/<int:aid>/<int:sid>')
def ignorespflag(aid,sid):
    query=text("""update sponser
                set flag=0
                where sid=:sid""")
    db.session.execute(query,{'sid':sid})
    db.session.commit()
    return redirect(f'/viewsp/{aid}')

@app.route('/flagspflag/<int:aid>/<int:sid>')
def flagspflag(aid,sid):
    query=text("""update sponser
                set flag=2
                where sid=:sid""")
    db.session.execute(query,{'sid':sid})
    db.session.commit()
    return redirect(f'/viewsp/{aid}')

@app.route('/ignoreinfflag/<int:aid>/<int:iid>')
def ignoreinfflag(aid,iid):
    query=text("""update influncer
                set flag=0
                where iid=:iid""")
    db.session.execute(query,{'iid':iid})
    db.session.commit()
    return redirect(f'/viewinf/{aid}')

@app.route('/flaginfflag/<int:aid>/<int:iid>')
def flaginfflag(aid,iid):
    query=text("""update influncer
                set flag=2
                where iid=:iid""")
    db.session.execute(query,{'iid':iid})
    db.session.commit()
    return redirect(f'/viewinf/{aid}')

@app.route('/viewcampad/<int:aid>/<int:cid>')
def viewcampad(aid,cid):
        query=text("""Select a.adid , c.name ,i.name ,a.status, a.payment
                from ad_request as a
                join influncer as i on a.influncer_id=i.iid
                join campaign as c on a.campaign_id=c.cid
                where c.cid=:cid""")
        result=db.session.execute(query,{'cid':cid})
        ads_all=result.fetchall()
        return render_template('viewads.html',aid=aid,ads_all=ads_all)

@app.route('/viewinfad/<int:aid>/<int:iid>')
def viewinfad(aid,iid):
        query=text("""Select a.adid , c.name ,i.name ,a.status, a.payment
                from ad_request as a
                join influncer as i on a.influncer_id=i.iid
                join campaign as c on a.campaign_id=c.cid
                where i.iid=:iid""")
        result=db.session.execute(query,{'iid':iid})
        ads_all=result.fetchall()
        return render_template('viewads.html',aid=aid,ads_all=ads_all)

@app.route('/viewspcamp/<int:aid>/<int:sid>')
def viewspcamp(aid,sid):
    query=text("""Select c.cid , c.name,s.name,c.visibilty ,s.flag
                from campaign as c
                join sponser as s on s.sid=c.sponser_id
                where s.sid=:sid""")
    result=db.session.execute(query,{'sid':sid})
    camp_all=result.fetchall()
    return render_template('viewcamp.html',aid=aid,camp_all=camp_all)

@app.route('/createadmin/<int:aid>',methods=['POST','GET'] )
def createadmin(aid):
    if request.method=='POST':
        ucreate=request.form['username']
        pcreate=request.form['password']
        newuser=Admin(name=ucreate,password=pcreate)

        try:
            db.session.add(newuser)
            db.session.commit()
            return redirect(f'/admindash/{aid}')
        except:
            return "error in creating"
    else:
        return render_template('createadmin.html',aid=aid)

if __name__ == "__main__":
    app.run(debug=True)