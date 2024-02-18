# Analytics Case - Travel acommodation bookings

DS role recruitment case. Solutions and aux code.  

## Assignment

Prepare a short presentation explaining what the data suggests in terms of: 
- the key drivers of Mobile performance, 
- where the opportunities in Mobile may lie. 

Please also consider what other data or information you would request, in order to gain additional insight.

## current ideas (backlog)

- super region to super region Sankey plot of net orders and net gross bookings
- YoY growth (orders and gross bookings)
- Mobile flag to explain uplift ("test"/causal effect)
  - mobile (all) vs. desktop
  - mobile app vs mobile web (exclude desktop)

## Extra Information that would be useful

- dimension of "Age range" of customers, to check for trends in mobile vs. desktop
- if it was customer level data, prior spending features would be useful
- number of cancelled orders and number of total orders would be usefull to calculate cancelling ratio and check for effects on it
- gross bookings of cancelled orders would also be interesting to understand if there is imbalance of avg. ticket and if this affects prob. of cancelling

## Notes about the dataset

### Inspection over dimensions

- `Week`: 
  - dates range from W45 to W48 (Nov)
  - years 2022 and 2023
  - can create a method to decompose string and get year/week date formats
- `Mobile indicator`:
  - either `Desktop` or `Mobile`
- `Platform types`:
  - Destkop ($35$k)
  - App (Mobile) $19$k
  - Web (Mobile) $18$k
- `Super Region`
  - APAC, EMEA, LATAM
  - many missing (`NaN`) values: all of them have country `US`
  - LATAM is undersampled, the others look uniform
- `Countries`
  - Total: $7$
  - `'Australia', 'Brazil', 'Hong Kong', 'Norway', 'South Korea', 'US', 'United Kingdom'`
  - $2$ APAC, $3$ EMEA, $1$ LATAM, $1$ NA
- `Property country`:
  - $207$ unique
  - US in top 5 destination of all super regions
  - Top destinations by net order
    - APAC: Australia, Japan, South Korea
    - EMEA: UK (by far), Norway, US
    - LATAM: Brazil (domestic, by far), US (second by far), Italy
    - North America: US (domestic, by far), Canada, Mexico
- `Booking Window Group`
  - string is a bit messy
  - represents bins of time-length (in days) between booking and check in
  - except for 1 category, looks uniformly distributed in sampling
  - "Post book" value: 
    - probably covers any booking activity that occurs post the initial check-in, 
    - contrasting with the other categories which all refer to the period before check-in
    - can fill "Post book" with -1 if it helps to turn this into numeric
    - only 40 rows, might as well discard

### inspection over facts (numerical columns)

Values are aggregated on the following dimensions tuple:  
`(Week, Device Type, Platform, Super Region, Country Name, Property Country, Booking Window Group)`

- `Net Gross Booking Value USD`
  - Definition: The total $ amount that customers pay to Hotels.com for their hotel reservation. The value of cancelled bookings is removed
  - some values are very negative (8.4% of rows)
    - from the definition, cancellations are removed (deducted), so it could explain it
    - 1319 out of 6200 have net orders positive
      - could this be result of discounts applied? 
      - by reading the definition ("amount that customers pay to") doesn't make much sense
  - US has the largest total bookings but lower avg. tickets
  - LATAM has very low total bookings but larger avg. ticket
  - APAC 2022 first week has double the avg. bookings and double avg. ticket, looks weird
- `Net Orders`
  - Definition: The total number of hotel bookings made - the number of bookings cancelled
  - some negative values 
  - negatives are fine because, by definition, bookings cancelled are subtracted

### Typical Values per Super Region:

Raw dataset, no cleaning.  
Range is related to avg. data from 2022 to 2023.

`APAC`*:
  - `Bookings`: $10$M - $14$M
  - `Orders`: $32$k - $51$k
  - `Ticket`: $\$320$ - $\$280$

\* if taking actual bookings first week 2022, it is 14M and avg. ticket $448

`EMEA`:
  - `Bookings`: $15$M - $19$M
  - `Orders`: $47$k - $64$k
  - `Ticket`: $\$332$ - $\$294$

`LATAM (Brazil)`:
  - `Bookings`: $4$M - $4$M
  - `Orders`: $9$k - $14$k
  - `Ticket`: $\$450$ - $\$291$

`North America (US)`:
  - `Bookings`: $73$M - $89$M
  - `Orders`: $295$k - $368$k
  - `Ticket`: $\$249$ - $\$241$


### explaining negative values of gross bookings and orders

By definition, cancellations will be deducted both in gross bookings as well as in transactions (orders) to calculate net values.  
Does larger booking order group (booking a lot in advance to checking in) is the main cause of net negative orders / negative gross bookings (more chances to cancel)?

- Confirmed larger frequency for net gross bookings (value counts when net gross bookings is negative)
  ```
    Booking Window Group
        +90 days      1472
        61-90 days    1152
        46-60 days     939
        15-30 days     782
        31-45 days     753
        8-14 days      532
        4-7 days       296
        2-3 days       155
        0-1 days       118
        Post Book        1
  ```
- Confirmed for net orders (value counts when net orders is negative)
```
   Booking Window Group
     +90 days      942
     61-90 days    702
     46-60 days    530
     31-45 days    414
     15-30 days    408
     8-14 days     249
     4-7 days      104
     2-3 days       32
     0-1 days       24
```

Thus, the insight is that there is a larger probability of cancelling when the Hotel is booked with a lot of time in advance before the check in date.
This should be better investigated to check for confounders and actual impact (maybe not a linear relationship).  
Also, "probability" of cancelling is not available in this aggregated data.

### APAC outlier 2022-W45

W45 of 2022 has double Net Gross Bookings USD for APAC region.
When we breakdown APAC 2022-W45 to identify why is it doubled in gross bookings, we find that
  - the source of the outlier is domestic Australia-Australia in Mobile App platforms
  - "Net Gross Booking Value USD" for this cohort is 100x above avg. of the following weeks
  - hard to explain it, because "Net Orders" doesn't have this spike, meaning avg. ticket goes 100x more expensive only in Mobile App ($27.4k vs. $271 in other weeks)
  - looks more like an aggregation error, probably duplicated source entries for this specific dimensions

So I'll assume it as an error, and treat/clean the gross bookings of this cohort dividing it by 100.  
Even doing that, avg. ticket for APAC 2022-W45 still looks a bit off.