# analytics_case_202402
DS role recruitment case. Solutions and aux code.  

## Assignment

Prepare a short presentation explaining what the data suggests in terms of: 
- the key drivers of Mobile performance, 
- where the opportunities in Mobile may lie. 

Please also consider what other data or information you would request, in order to gain additional insight.


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
  - Thailand and UK top 5 for both APAC and EMEA
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

