import sqlite3, folium, pandas, os
import matplotlib.pyplot as plt
m = folium.Map(location=[53.5444,-113.323], zoom_start=11)

def bar(conn):
    # Given: range of years + crime type
    # Show: bar plot of month-wise total counts of the crime
    c = conn.cursor()
    # get inputs
    start = input("Start year:")
    end = input("End year:")
    # get crime types
    c.execute("select distinct crime_type from crime_incidents")
    crimes = c.fetchall()
    crime = input("Select a crime: [{}] \n".format(crimes))
    print(crime)
    # displaying chart
    df = pandas.read_sql_query('''select crime_type, month, count(*)
                from crime_incidents
                where crime_type = "{}" and year between {} and {}
                group by month
                '''.format(crime,start,end), conn)
    print(df)
    plot = df.plot.bar(x="Month")
    plt.plot()
    plt.show()


def map(conn):
    # Given: range of years + crime type + integer N
    # Show: map of the top-N neighborhoods with the crime type + their occurances in the range of years
    c = conn.cursor()
    # get inputs
    start = input("Start year:")
    end = input("End year:")
    amt = input("Enter number of neighbourhoods:")
    # get crime types
    c.execute("select distinct crime_type from crime_incidents")
    crimes = c.fetchall()
    crime = input("Select a crime: [{}]\n".format(crimes))

    # query for data based on input
    c.execute('''
                select coordinates.neighbourhood_name, sum(Incidents_count), latitude, longitude
from crime_incidents, coordinates
where year between {} and {}
and crime_type = "{}"
and coordinates.Neighbourhood_Name = crime_incidents.Neighbourhood_Name
group by coordinates.neighbourhood_name
having sum(Incidents_count) >= (select min(inc)
from 
(select sum(Incidents_count) as inc
                from crime_incidents, coordinates
                where year between {} and {}
                    and crime_type = "{}"
					and coordinates.Neighbourhood_Name = crime_incidents.Neighbourhood_Name
                group by coordinates.neighbourhood_name
                order by sum(Incidents_count) desc
				limit {}))
order by sum(Incidents_count) desc
            '''.format(start,end,crime,start,end,crime,amt))

    nHood = c.fetchall()
    print(nHood)
    # iterate through tuples and add them to map
    for i in range(len(nHood)):
        nName = nHood[i][0]
        amtCrime = nHood[i][1]
        Latitude = float(nHood[i][2])
        Longitude = float(nHood[i][3])
        folium.Circle(location=[Latitude, Longitude], popup= nName + '<br>' + str(amtCrime), radius = amtCrime*2, color= 'crimson',fill= True, fill_color= 'crimson').add_to(m)


    num = 1
    while os.path.isfile("Map-{}.html".format(num)):
        num = num + 1
    m.save('Map-{}.html'.format(num))
    print('Map saved')
