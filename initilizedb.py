from app import app, db
from app import Sponser,Influncer,Admin, ad_request, Campaign
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from sqlalchemy import text


sponsor1 = Sponser(name="sname", password="spass", budget=5000)
sponsor2 = Sponser(name="EcoLife", password="password456", budget=8000)
sponsor3 = Sponser(name="GourmetBites", password="password789", budget=12000)
sponsor4 = Sponser(name="FitnessPro", password="password101", budget=7000)
sponsor5 = Sponser(name="EduMaster", password="password202", budget=6000)

influencer1 = Influncer(name="iname", password="ipass", follower=15000, Niche="tech")
influencer2 = Influncer(name="Bob Brown", password="password456", follower=25000, Niche="fitness")
influencer3 = Influncer(name="Charlie Davis", password="password789", follower=18000, Niche="gaming")
influencer4 = Influncer(name="Dana Lee", password="password101", follower=22000, Niche="beauty")
influencer5 = Influncer(name="Eva Green", password="password202", follower=30000, Niche="travel")
influencer6 = Influncer(name="Frank Harris", password="password303", follower=20000, Niche="food")
influencer7 = Influncer(name="Grace Kim", password="password404", follower=16000, Niche="education")
influencer8 = Influncer(name="Henry Lewis", password="password505", follower=14000, Niche="lifestyle")
influencer9 = Influncer(name="Ivy Martinez", password="password606", follower=25000, Niche="misc")
influencer10 = Influncer(name="Jack Wilson", password="password707", follower=19000, Niche="tech")

campaign1 = Campaign(name="Tech Innovations", sponser_id=1, Description="Campaign for new tech products.", visibilty=0, start_date=datetime(2024, 8, 10), end_date=datetime(2024, 9, 10))
campaign2 = Campaign(name="Green Future", sponser_id=2, Description="Campaign for eco-friendly initiatives.", visibilty=1, start_date=datetime(2024, 8, 15), end_date=datetime(2024, 10, 15))
campaign3 = Campaign(name="Taste of the World", sponser_id=3, Description="Campaign promoting gourmet foods.", visibilty=0, start_date=datetime(2024, 9, 1), end_date=datetime(2024, 11, 1))
campaign4 = Campaign(name="Fit Life", sponser_id=4, Description="Campaign for fitness products and services.", visibilty=1, start_date=datetime(2024, 9, 15), end_date=datetime(2024, 12, 15))
campaign5 = Campaign(name="Learning Made Easy", sponser_id=5, Description="Campaign for educational tools and resources.", visibilty=0, start_date=datetime(2024, 10, 1), end_date=datetime(2024, 12, 1))

ad1=Admin(name="aname",password="apass")

with app.app_context():
    # db.create_all()
    # with db.session.begin():
    #     db.session.add_all([sponsor1, sponsor2, sponsor3, sponsor4, sponsor5,
    #                     influencer1, influencer2, influencer3, influencer4, influencer5,
    #                     influencer6, influencer7, influencer8, influencer9, influencer10,
    #                     campaign1, campaign2, campaign3, campaign4, campaign5 ,ad1])
    #     db.session.commit()
    query=text("""select * from Sponser""")
    res=db.session.execute(query)
    a=res.fetchall()
    print(a)
        # print("all commited")
