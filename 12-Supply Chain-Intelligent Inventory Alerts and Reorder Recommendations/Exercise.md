# Question 08: Smart warning of stockpiles and recommendations for replenishment

# Background

An electrician enterprise manages multiple warehouses and hundreds of SKU. Procurement teams need to determine on a daily basis which commodities may be cut off before new shipments arrive, which commodities are below safe stock, which commodities are surplus or deselling... The data are larger and there are promotion days, zero sales and missing sales records on some dates.

You are a member of the Digitalistic Stockpile Operation project, which requires the construction of a smart body capable of calculating the health of the inventory in bulk, predicting the time of the stock cut and generating replenishment or stocking recommendations.

# Provide material

- `Inventory data.csv ': 520 existing SKU stocks, secure stocks, in-transit stocks, procurement lead times and minimum orders...
- `Data on sales for nearly 30 days.csv ': approximately 15,000 daily sales records...
- `Alarm rules.txt ': average daily sales, stock supporting days, classification, replenishment, cut-off date and round-up rules...

# Business tasks to be accomplished

1. Processing of all 520 SKUs, calculated as valid sales days, average daily sales and stock supporting days, based on SKU associated inventory and sales data.
2. SKU is classified strictly as emergency replenishment, recommended replenishment, normal stock, surplus stock, de-sale/zero sales or missing data...
3. For SKU to replenish, the target inventory is calculated by deducting the amount of stock available and stock in transit and by taking it upwards to the minimum order... and by exporting the emergency level and the expected date of the stock cut.
4. Export inventory health breakdown and breakdown, at least by warehouse, commodity category, supplier and emergency level...
5. Draft procurement request for SKU to be replenished; list of actions to generate sales promotion, redeployment or liquidation of excess SKU, but not to execute procurement or promotion on its own.

# Unusual and border

- When a valid sales record is less than 25 days, the tag "data" is missing, and no replenishment is calculated.
- The average daily sales volume is 0-hour mark "demurrage/zero sales" and may not be divided by 0 or generate recommendations for regular replenishment.
- The volume of the returned goods is not directly deducted from the sales; additional qualitative risk tips may be provided when required.
- The food beverages should be indicated as a guarantee period risk, but the material does not provide a batch period and no forward quantity may be inferred.
- The date of the cut-off should be recalculated and correctly updated after the date of the change of data or new sales data.

# Delivery requirements

On-site demonstration of volume calculations, six types of results, minimum order volume fixes, data missing and zero volume processing.
