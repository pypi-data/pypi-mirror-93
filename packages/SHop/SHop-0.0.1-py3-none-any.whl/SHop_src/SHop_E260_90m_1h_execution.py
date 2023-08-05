# PAQUETES PARA CORRER OP.
import pandas as pd
import numpy as np
import datetime as dt
import json
import wmf.wmf as wmf
import hydroeval
import glob
import MySQLdb
#modulo pa correr modelo
import SHop
import hidrologia

#FORMATO
# fuente
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
import matplotlib.font_manager as font_manager
font_dirs = ['/home/socastillogi/jupyter/fuentes/AvenirLTStd-Book']
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)
matplotlib.rcParams['font.family'] = 'Avenir LT Std'
matplotlib.rcParams['font.size']=12
import pylab as pl 
#axes
pl.rc('axes',labelcolor='#4f4f4f')
pl.rc('axes',linewidth=1.5)
pl.rc('axes',edgecolor='#bdb9b6')
pl.rc('text',color= '#4f4f4f')
# pl.rc('xtick',color='#4f4f4f')
# pl.rc('ytick',color='#4f4f4f')
# pl.locator_params(axis='y', nbins=5)
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)


############################################################################################  ARGUMENTOS

#configfile horario
ruta_proj = '/home/socastillogi/jupyter/ensayos/SHop/SHop_E260_90m_1h/'
configfile=ruta_proj+'static_inputs/configfile_SHop_SM_E260_1h.md'
save_hist = True 
date = '2020-11-28 22:13'#dt.datetime.now().strftime('%Y-%m-%d %H:%M')
ConfigList= SHop.get_rutesList(configfile)

#configfile diario
ruta_proj_d = '/home/socastillogi/jupyter/ensayos/SHop/SHop_E260_90m_1d/'
configfile_d=ruta_proj_d+'static_inputs/configfile_SHop_SM_E260_1d.md'
ConfigList_d= SHop.get_rutesList(configfile_d)

############################################################################################ EJECUCION


# abrir simubasin
path_ncbasin = SHop.get_ruta(ConfigList,'ruta_proj')+SHop.get_ruta(ConfigList,'ruta_nc')
cu = wmf.SimuBasin(rute=path_ncbasin)
#sets para correr modelo.
SHop.set_modelsettings(ConfigList)
warming_steps =  5*24#pasos de simulacion no seg, dependen del dt.
warming_window ='%ss'%int(wmf.models.dt * warming_steps) #siempre en seg
dateformat_starts = '%Y-%m-%d %H'
dateformat_binrain = '%Y%m%d%H%M'

#definicion de ventanas
starts  = ['%ss'%(0),'%ss'%(0)]
starts_names = ['1d','1d'] #starts y windows deben ser del mismo len.
window_end = '%ss'%(0*24*60*60) #hora actual

#definicion de executionprops
df_executionprops_h = pd.DataFrame([starts,
                                  starts_names,
                                  ['%s-p01-ci1-90d.StOhdr'%(SHop.get_ruta(ConfigList_d,'ruta_proj')+SHop.get_ruta(ConfigList_d,'ruta_sto_op')),
                                  'reglas_pant'],
                                  ['ci2','ci3'],
                                  #[1.0 , 5.9 , 5.7 , 0.0 , 1.0 , 1.0 , 10.8 , 1.0 , 1.0 , 1.0 ],
                                  [[0.8 , 10 , 17.7 , 0.0 , 9.0 , 2.0 , 15 , 0.9 , 1.0 , 1.0, 1.0 ],
                                   [0.8 , 10 , 17.7 , 0.0 , 9.0 , 2.0 , 15 , 0.9 , 1.0 , 1.0, 1.0 ]],
#                                    [0.8,  8.5, 13,    0.0,  9.0,  2.0,   4,     1,    1,    1,  1]
                                  ['-p01','-p01'],
                                  [0,0]], #pasos de sim, depende de dt
                                 columns = [1,2],
                                 index = ['starts','start_names','CIs','CI_names','pars','pars_names','wup_steps']).T

print ('#########################')
print ('Start HOURLY execution: %s'%dt.datetime.now())    
#ventanas de tiempo en que se correra


#dates
start_o = pd.to_datetime(pd.to_datetime(date).strftime('%Y-%m-%d')) - pd.Timedelta('2d')#arranca desde las 00 del dia anterior para tener 1d de calentamiento.

starts_w_h = [start_o - pd.Timedelta(start) for start in starts]
starts_m_h = [start_w_h - pd.Timedelta(warming_window) for start_w_h in starts_w_h]
end_h = pd.to_datetime(pd.to_datetime(date).strftime(dateformat_starts)) + pd.Timedelta(window_end)


# rainfall  : takes 3min
pseries,ruta_out_rain_h = SHop.get_rainfall2sim(ConfigList,cu,path_ncbasin,[starts_m_h[0]],end_h, #se corre el bin mas largo.
                                             Dt= float(wmf.models.dt),include_escenarios=None,
                                             evs_hist= False,
                                             check_file=True,stepback_start = '%ss'%int(wmf.models.dt*1),
                                             complete_naninaccum=True,verbose=False)

print (ruta_out_rain_h)

SHop.set_modelsettings(ConfigList)
# set of executions
ListEjecs_h =  SHop.get_executionlists_fromdf(ConfigList,ruta_out_rain_h,cu,starts_m_h,end_h,df_executionprops_h,
                                         warming_steps=warming_steps, dateformat_starts = dateformat_starts,
                                         path_pant4rules = ruta_out_rain_h)

# #execution
print ('Start simulations: %s'%dt.datetime.now())
print ('start: %s - end: %s'%(starts_m_h[0], end_h))
SHop.set_modelsettings(ConfigList)
res = SHop.get_qsim(ListEjecs_h[:],set_CI=True,save_hist=save_hist,verbose = True)
print ('End simulations: %s'%dt.datetime.now())

############################################################################################ GRAFICAS


#REVISAR CAUDAL.
#tramos, para sacar los datos del modelo.
df_tramos = pd.read_csv(SHop.get_ruta(ConfigList,'ruta_proj')+SHop.get_ruta(ConfigList,'ruta_nc_tramos'),index_col=0)
ests = df_tramos.index
#curvas que escogí.
df_est_features = pd.read_csv(SHop.get_ruta(ConfigList,'ruta_proj')+SHop.get_ruta(ConfigList,'ruta_curvascalob3'),index_col=0)
ests = df_est_features.index
tramos_ids = np.concatenate(df_tramos.loc[ests].values)
df_est_features['tramo'] = list(map(str,tramos_ids))

#df con metadatos de estaciones
#METADATOS BD
server,user,passwd,dbname = SHop.get_credentials(SHop.get_ruta(ConfigList,'ruta_proj')+SHop.get_ruta(ConfigList,'ruta_credenciales'))

conn_db = MySQLdb.connect(server,user,passwd,dbname)
db_cursor = conn_db.cursor ()
query = 'select codigo,nombreestacion,longitude,latitude,estado from estaciones where codigo in ("%s","%s","%s","%s","%s","%s","%s","%s","%s");'%(ests[0],ests[1],ests[2],ests[3],ests[4],ests[5],ests[6],ests[7],ests[8])#,"%s","%s","%s","%s"

db_cursor.execute (query)
data = db_cursor.fetchall()
conn_db.close()
fields = [field.lower() for field in list(np.array(db_cursor.description)[:,0])]
df_bd = pd.DataFrame(np.array(data), columns = fields)
df_bd['codigo'] = list(map(int,df_bd['codigo']))
df_bd = df_bd.set_index('codigo')

#OTROS ARGS
start = starts_w_h[0]
end= end_h
Dt = '1h'
colors_d = ['lightgreen','g']#['c','darkblue']#
ylims = [10,40,40,100,300,200,300]

path_r = ruta_out_rain_h.split('.')[0]+'.hdr'
path_masks_csv = SHop.get_ruta(ConfigList,'ruta_proj')+SHop.get_ruta(ConfigList,'ruta_csv_subbasinmask')

rutafig = SHop.get_ruta(ConfigList,'ruta_proj')+SHop.get_ruta(ConfigList,'ruta_qsim_png')


#GRAFICA
SHop.plot_Q(start,end,Dt,server,user,passwd,dbname,
            ListEjecs_h,cu,ests,colors_d,path_r,path_masks_csv,
            df_bd,df_est_features,ylims,rutafig=rutafig)