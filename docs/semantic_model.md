# TSQLV6 Semantic Layer

## Sales.OrderValues

Purpose:
Pre-calculated order level metrics.

Grain:
One row per order.

Columns:
- orderid
- custid
- empid
- shipperid
- orderdate
- requireddate
- shippeddate
- qty
- val

Use for:
- Revenue analysis
- Order value analysis
- Average order size
- Sales totals

---

## Sales.EmpOrders

Purpose:
Monthly employee performance summary.

Grain:
One row per employee per month.

Columns:
- empid
- ordermonth
- val
- numorders

Use for:
- Employee rankings
- Monthly sales performance
- Top salespeople
- Order volume by employee

---

## Sales.CustOrders

Purpose:
Monthly customer purchasing activity.

Grain:
One row per customer per month.

Columns:
- custid
- ordermonth
- qty

Use for:
- Customer activity
- Purchasing trends
- Top customers

---

## Sales.OrderTotalsByYear

Purpose:
Yearly sales summaries.

Grain:
One row per year.

Columns:
- orderyear
- qty

Use for:
- Year-over-year analysis
- Historical trends
- Annual reporting

---

# Relationships

Sales.Customers (1)
    -> Sales.Orders (many)

HR.Employees (1)
    -> Sales.Orders (many)

Sales.Shippers (1)
    -> Sales.Orders (many)

Sales.Orders (1)
    -> Sales.OrderDetails (many)

Production.Products (1)
    -> Sales.OrderDetails (many)

Production.Suppliers (1)
    -> Production.Products (many)

Production.Categories (1)
    -> Production.Products (many)

Stats.Tests (1)
    -> Stats.Scores (many)

HR.Employees (Manager)
    -> HR.Employees (Subordinate)