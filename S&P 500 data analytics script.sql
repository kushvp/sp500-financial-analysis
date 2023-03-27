create database sp500;
use sp500;

#------------------------------------------------------------------------------------------
# Data Loading scripts
#------------------------------------------------------------------------------------------
SET GLOBAL local_infile=1;

LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/stocks.csv'
INTO TABLE stocks
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

#------------------------------------------------------------------------------------------
# Data Verification
#------------------------------------------------------------------------------------------

select * from sp500.companies;
select * from sp500.financials_old;
select * from sp500.financials_new;
select * from sp500.price_movement;
select * from sp500.sp500_price_movement;

desc sp500.companies;
desc sp500.financials_old;
desc sp500.financials_new;
desc sp500.price_movement;
desc sp500.sp500_price_movement;

#------------------------------------------------------------------------------------------
# Insights Queries
#------------------------------------------------------------------------------------------

# GOOG monthly adj_close price and moving average
select date_format(tab.date, '%Y-%m') as month, tab.adj_close, 
avg(tab.adj_close) over(ORDER BY tab.date ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) 'MV2'
from (select s.date, s.adj_close,ROW_NUMBER() OVER (PARTITION BY YEAR(s.date), Month(s.date) ORDER BY s.date DESC) 'RowRank' 
from sp500.price_movement s where s.symbol='GOOG') tab where tab.RowRank = 1
group by date_format(tab.date, '%Y-%m') order by date_format(tab.date, '%Y-%m') desc;

# GOOG daily 20 and 50 day moving average since 2020
select s.date,s.volume,s.adj_close,case when row_number() over w20 > 19 then avg(s.adj_close) over w20 end 'MV20',
case when row_number() over w50 > 49 then avg(s.adj_close) over w50 end 'MV50'
from sp500.price_movement s where s.symbol='GOOG' and s.date>'2020-01-01'
window w20 as (ORDER BY s.date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW),
w50 as (ORDER BY s.date ROWS BETWEEN 49 PRECEDING AND CURRENT ROW);

# Company Rating based on Average Price to Earning of corresponding Sector
select c.name,c.sector,f.pe,avg(f.pe) over(partition by c.sector) sector_avg,
case when f.pe>avg(f.pe) over(partition by c.sector) || f.pe<0 then "Overvalued" else "Undervalued" end rating 
from sp500.companies c join sp500.financials_new f on f.symbol=c.symbol
order by c.sector,f.pe;

# Company Rating based on Average Revenue Growth of corresponding Sector
select c.name,c.sector,c.revenue_growth *100 revenue_growth,avg(c.revenue_growth) over(partition by c.sector) *100 sector_avg,
case when c.revenue_growth>avg(c.revenue_growth) over(partition by c.sector) then "Outperformance" else "Underperformance" end rating
from sp500.companies c
order by c.sector,c.revenue_growth desc;

# PE and Revenue growth combined
select * from (select c.name, c.sector, avg(f.pe) over(partition by c.sector) sector_avg_pe, f.pe,
case when f.pe>avg(f.pe) over(partition by c.sector) || f.pe<0 then "Overvalued" else "Undevalued" end pe_rating, 
case when c.revenue_growth>avg(c.revenue_growth) over(partition by c.sector) then "Outperformance" 
else "Underperformance" end growth_rating,c.revenue_growth *100 growth,avg(c.revenue_growth) over(partition by c.sector) *100 sector_avg_growth
from sp500.companies c join sp500.financials_new f on f.symbol=c.symbol) tab
where tab.pe_rating="Undevalued" and tab.growth_rating="Outperformance"
order by tab.sector,tab.growth/pe desc;

# Group by industry and order them by their market cap
select c.sector,c.industry, sum(c.market_cap) from sp500.companies c
group by c.sector,c.industry order by sum(c.market_cap) desc;

# Sector market cap contribution in each State
select tab.st,tab.sec,tab.mcap,
sum(tab.mcap) over(partition by tab.st), (tab.mcap/sum(tab.mcap) over(partition by tab.st))*100
from (SELECT c.state st, c.sector sec, sum(c.market_cap) mcap from sp500.companies c
GROUP BY c.state, c.sector) tab 
order by tab.st,tab.mcap desc;

# Top Sector in each State based on Total Market Cap ranking
select c.state, c.sector, sum(c.market_cap) as state_sector_mcap,
rank() over(partition by c.state order by sum(c.market_cap) desc) as state_sector_rank
from sp500.companies c
where c.state is not null
group by c.state,c.sector;

# Top State in each Sector based on Total Market Cap ranking
select c.sector, c.state,sum(c.market_cap) as total_mcap,
rank() over (partition by c.sector order by sum(c.market_cap) desc) as state_rank
from sp500.companies c where c.state is not null
group by c.sector,c.state
order by sum(c.market_cap) desc;
