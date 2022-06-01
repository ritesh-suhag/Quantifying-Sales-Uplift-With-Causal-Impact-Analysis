
##############################################################################
# CASUAL IMPACT ANALYSIS
##############################################################################

# ~~~~~~~~~~~~~~~~~~~~~~~~ IMPORT REQUIRED PACKAGES ~~~~~~~~~~~~~~~~~~~~~~~~~~

from causalimpact import CausalImpact
import pandas as pd

# ~~~~~~~~~~~~~~~~~~~~~~~~~ IMPORT AND CREATE DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~

# IMPORT DATA TABLES

transactions = pd.read_excel("data/grocery_database.xlsx", sheet_name = "transactions")
campaign_data = pd.read_excel("data/grocery_database.xlsx", sheet_name = "campaign_data")

# AGGREGATE TRANSACTIONS DATA TO CUSTOMER, DATE LEVEL

customer_daily_sales = transactions.groupby(["customer_id", "transaction_date"])["sales_cost"].sum().reset_index()

# MERGE ON THE SIGNUP FLAG

customer_daily_sales = pd.merge(customer_daily_sales, campaign_data, how = "inner", on = "customer_id")

# PIVOT THE DATA TO AGGREGATE DAILY SALES BY SIGNUP GROUP

causal_impact_df = customer_daily_sales.pivot_table(index = "transaction_date",
                                                    columns = "signup_flag",
                                                    values = "sales_cost",
                                                    aggfunc = "mean")

# PROVIDE A FREQUENCY FOR OUR DATETIMEINDEX (AVOIDS A WARNING MESSAGE)

causal_impact_df.index
# Since the freq = None, we can specify it using - 
causal_impact_df.index.freq = "D"

# FOR CAUSAL IMPACT WE NEED THE IMPACTED GROUP IN THE FIRST COLUMN

causal_impact_df = causal_impact_df[[1,0]]

# RENAME COLUMNS TO SOMETHING MORE MEANINGFUL

causal_impact_df.columns = ["member", "non_member"]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ APPLY CAUSAL IMPACT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Before we start the algorithm we need to specify the start and the end date.
pre_period = ["2020-04-01", "2020-06-30"]
post_period = ["2020-07-01", "2020-09-30"]

ci = CausalImpact(causal_impact_df, pre_period, post_period)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PLOT THE IMPACT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ci.plot()

# ~~~~~~~~~~~~~~~~ EXTRACT THE SUMMARY STATISTICS AND REPORT ~~~~~~~~~~~~~~~~~

print(ci.summary())

# To get the report - 
print(ci.summary(output = "report"))
