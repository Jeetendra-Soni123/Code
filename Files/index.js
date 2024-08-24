let x = fetch("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo").then(async (c)=>{
    j = await c.json()
    console.log(j)
})