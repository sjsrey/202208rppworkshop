from geosnap import Community
import geopandas
import tobler

sd = Community.from_census(county_fips='06073')
gdf = sd.gdf
gdf = gdf[gdf.year == 2010]


def choropleth(gdf, variable, scheme='quantiles', k=5,
               figsize=(16, 9)):
    ax = gdf.plot(column=variable,
                  scheme=scheme,
                  k=k,
                  figsize=figsize,
                  edgecolor='grey',
                  legend=True, linewidth=0.5)
    ax.set_axis_off()
    ax.set_title(variable)
    return ax


def explore(gdf, variable,
            scheme='quantiles',
            k=5,
            cmap='viridis'):
    return gdf.explore(column=variable,
                       tooltip=[variable],
                       scheme=scheme,
                       k=k,
                       cmap=cmap)


def choro3(gdf, var1, var2, var3):
    from matplotlib import pyplot
    fig, (ax1, ax2, ax3) = pyplot.subplots(ncols=3,
                                           sharex=True,
                                           sharey=True,
                                           figsize=(16, 9))
    gdf.plot(ax=ax1, column=var1, scheme='quantiles', k=5)
    gdf.plot(ax=ax2, column=var2, scheme='quantiles', k=5)
    gdf.plot(ax=ax3, column=var3, scheme='quantiles', k=5)
    ax1.set_axis_off()
    ax1.set_title(var1)
    ax2.set_axis_off()
    ax2.set_title(var2)
    ax3.set_axis_off()
    ax3.set_title(var3)
    return fig


roads = geopandas.read_file("zip://./data/tl_2015_06_prisecroads.zip")


# set crs

roads = roads.to_crs(gdf.estimate_utm_crs())
gdf = gdf.to_crs(gdf.estimate_utm_crs())

sd_county = gdf.unary_union

sd_freeways = geopandas.clip(roads, sd_county)


b1000 = sd_freeways.buffer(304.8)
b1000uu = b1000.unary_union


# interpolation


target = geopandas.GeoDataFrame(geometry=[b1000uu])
target.crs = gdf.crs

extensive_variables = ['n_total_pop',
                       'n_nonhisp_white_persons',
                       'n_hispanic_persons',
                       'n_nonhisp_black_persons'
                       ]
ae = tobler.area_weighted.area_interpolate
estimates = ae(source_df=gdf, target_df=target,
               extensive_variables=extensive_variables, allocate_total=False)

county_population = gdf[extensive_variables].sum()
county_composition = county_population / county_population[0]


buffer_population = estimates

eev = estimates[extensive_variables]
buffer_composition = eev.div(estimates['n_total_pop'], axis=0)

def choro3roads(gdf=gdf, roads=b1000, var1='p_nonhisp_white_persons',
                var2='p_hispanic_persons',
                var3='p_nonhisp_black_persons'):

    from matplotlib import pyplot
    fig, (ax1, ax2, ax3) = pyplot.subplots(ncols=3,
                                           sharex=True,
                                           sharey=True,
                                           figsize=(16, 9))
    gdf.plot(ax=ax1, column=var1, scheme='quantiles', k=5)
    roads.plot(ax=ax1, color='white')
    gdf.plot(ax=ax2, column=var2, scheme='quantiles', k=5)
    roads.plot(ax=ax2, color='white')
    gdf.plot(ax=ax3, column=var3, scheme='quantiles', k=5)
    roads.plot(ax=ax3, color='white')
    ax1.set_axis_off()
    ax1.set_title(var1)
    ax2.set_axis_off()
    ax2.set_title(var2)
    ax3.set_axis_off()
    ax3.set_title(var3)
    return fig

