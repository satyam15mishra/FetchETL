#What are the top 5 brands by receipts scanned for most recent month?

select distinct b.name, count(r.receipt_id), r.purchaseDate, MAX(strftime('%Y-%m', purchaseDate)) AS latest_month
from receipts r
left join brands b
on b.brandCode = r.brandCode
where b.name != '' and purchaseDate != ''
group by b.brandCode
order by count(r.receipt_id) desc, r.purchaseDate desc
limit 6

# When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?

select rewardsReceiptStatus, avg(totalSpent) 
from receipts 
group by rewardsReceiptStatus

#When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
select rewardsReceiptStatus, sum(purchasedItemCount) as totalPurchasedItems from receipts
group by rewardsReceiptStatus


#Which brand has the most spend among users who were created within the past 6 months?
select b.brandCode, b.name, sum(r.totalSpent)
from brands b
left join receipts r 
on r.brandCode = b.brandCode
left join users u on u.userid = r.userId
where b.brandCode != '' and u.createDate >= (SELECT DATE(MAX(createDate), '-6 months') FROM users)
group by b.brandCode
order by sum(r.totalSpent) desc limit 3