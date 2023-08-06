import time
import scipy
import pickle
import numpy as np
import pandas as pd
import velocyto as vcy
import os
import scanpy as scp
import anndata as ann
import matplotlib.pyplot as plt 
import gc
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib_venn as ven
from matplotlib.gridspec import GridSpec
import sklearn
from sklearn.decomposition import PCA
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, accuracy_score, cohen_kappa_score, confusion_matrix, recall_score, classification_report, precision_score
from scipy.stats import spearmanr, zscore, kstest, ks_2samp
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import Lasso, Ridge, ElasticNet

from sklearn.svm import SVC
from sklearn.metrics import mutual_info_score
def plot_genes_r2_phase_portrait_supp_hb(path, vlm, df, genes, figname):
  leidens = np.unique(vlm.ca["leiden"])
  # color = ["crimson", "deeppink", "dodgerblue", "green", "darkorange"]
  color = sns.hls_palette(len(set(leidens)), l=0.5, s=0.8)
  ncol = len(leidens)+1
  nrow = len(genes)
  w = 4*ncol
  h = 4*nrow
  fig = plt.figure(figsize=(w,h))
  gs = GridSpec(nrows=nrow, ncols=ncol, hspace=0.3, wspace=0.3)
  i=0

  for g in genes:
    try:
      idx = np.where(vlm.ra["var_names"]==g)[0][0]
    except:
      pass

    k=0
    c=0
    # plot phase portrait

    for d in leidens:

      samples = vlm.ca["leiden"]==d
      ax = fig.add_subplot(gs[i,k])
      plt.scatter(vlm.Sx_sz[idx,samples], vlm.Ux_sz[idx,samples], s=50, c=color[c], alpha=0.5)
      xnew = np.linspace(0, (vlm.Sx_sz[idx,samples]).max()+0.01)
      plt.plot(xnew, vlm.gammas[idx]*(xnew)+vlm.q[idx], color="k", linewidth=1)
      # plt.ylabel("u", fontsize=11)
      # plt.xlabel("s", fontsize=11)
      ax.spines['right'].set_visible(False)
      ax.spines['top'].set_visible(False)
      plt.title(f'cluster {d}', loc='center')
      k+=1
      c+=1

    # plot r-squared
    skip_col=-2
    ix = np.where(df.index==g)[0][0]
    ax = fig.add_subplot(gs[i,k])
    temp = df.iloc[ix,:skip_col].values<0
    h=0.6
    plt.barh(df.columns[:skip_col][~temp], df.iloc[ix,:skip_col][~temp], height=h, color='dodgerblue',  )
    plt.barh(df.columns[:skip_col][temp], df.iloc[ix,:skip_col][temp], height=h, color='#d60000',  )
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.invert_yaxis()
    # plt.xlim(np.min(sigd.iloc[idx,:-2])-0.5, 1.5)
    # plt.xticks(ticks=[-5,-3,0,1], label=[-5,-3,0,1])
    plt.ylabel("clusters")
    plt.xlabel("R2")
    plt.title(g, loc='center')

    k+=1
    i+=1
  if figname:
    plt.savefig(path['save']+f"{g}_hb_phase_portrait.pdf", bbox_inches='tight', dpi=600)
  else:
    plt.savefig(path['save']+"hb_phase_portrait.pdf", bbox_inches='tight', dpi=600)

def violin_plotting(path,r2,per=.1):
	da=[]
	lab=[]
	celltype = r2.columns
	for ct in celltype:
	    # print(ct)
	    x=r2.loc[:,ct]
	    x=np.sort(x)
	    x=x[int(len(x)*(1-per)):-1]
	    da.extend(x)
	    y=[ct]*len(x)
	    lab.extend(y)
	df=pd.DataFrame({"data":da,"lab":lab})
	############################################################
	# get mis matrix 
	"""da=[]
	lab=[]
	for ct in celltype:
	    # print(ct)
	    x=mis.loc[:,ct]
	    x=np.sort(x)
	    x=x[int(len(x)*0):-1]
	    da.extend(x)
	    y=[ct]*len(x)
	    lab.extend(y)
	df1=pd.DataFrame({"data":da,"lab":lab})"""
	plt.subplot(1,1,1,position=[0,0,3,1])
	a=sns.violinplot(x="lab", y="data", data=df)
	plt.title("Clusters with Rsquared")
	plt.ylabel("Rsquared Score")
	plt.xlabel("clusters")
	a.set_xticklabels(a.get_xticklabels(),rotation=30)
	"""plt.subplot(2,2,2,position=[2.25,0,2,1])
	b=sns.violinplot(x="lab", y="data", data=df1)
	plt.title("Clusters with Mutual Information")
	plt.ylabel("Mutual Information Score")
	plt.xlabel("clusters")
	b.set_xticklabels(b.get_xticklabels(),rotation=30)
	plt.savefig(path['save']+"violin_plot.pdf", bbox_inches='tight', dpi=600)"""

"""def count_genes():
	sigi = pd.read_csv(path["sigi"], index_col=0)
	sigd = pd.read_csv(path["sigd"], index_col=0)
	print(sigi.shape, sigd.shape)
	df = pd.DataFrame(columns = ['Count', 'Genes'])
	newrow = {
	    'Count': sigd.shape[0],
	    'Genes': 'Breakdown'
	}

	df = df.append(newrow, ignore_index=True)
	newrow = {
	    'Count': sigi.shape[0],
	    'Genes': 'Restoration'
	}
	df = df.append(newrow, ignore_index=True)
	print(df)
	sns.catplot(x='Genes', y='Count', data=df, kind='bar', palette='viridis', height=4, aspect=0.7)
	plt.savefig(path['save']+'fig_C.pdf', bbox_inches='tight', dpi=600)"""
		
"""def r2_cut(path, r_c, r2):
	leidens = [int(i) for i in r2.columns]
	count = (r2<r_c).sum(0).values
	# print(count)
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	plt.plot(leidens, count, "o-", c='crimson')
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	plt.xlabel('leidens')
	plt.ylabel('Gene count')
	plt.savefig(path['save']+'fig_B.pdf', bbox_inches='tight', dpi=600)"""

"""def getting_cor(r2,pv,co):
	# find spearman correlation and associated 2 tailed p-value
	cor = np.zeros(r2.shape[0], dtype=float)
	pval = np.zeros(r2.shape[0], dtype=float)
	# time = [1,2,3,4,5]
    time = list(range(len(r2.columns)))
	for i in range(r2.shape[0]):
	  cor[i,], pval[i,] = spearmanr(a=r2.iloc[i,:].values, b=time) # correlation, pval

	print(len(r2.index))
	print(len(r2.index.unique()))
	print(len(cor))
	print(len(pval))
	print("significant genes", (pval<=pv).sum())
	print("restoration genes", ((pval<=pv) & (cor>co)).sum())
	print("homeostasis breakdown genes", ((pval<pv) & (cor<-co)).sum())

	# monotonically decreasing genes/ homeostasis breakdown genes
	temp = ((pval<pv) & (cor<=-co))
	print(len(temp))
	genes = r2.index[temp]

	sig = r2.loc[temp,:]
	sig['spcor'] = cor[temp]
	sig['pval'] = pval[temp]
	print(sig.shape)
	# print(sig.head())
	# save breakdown genes
	sig_br=sig
	sig.to_csv(path["sigd"])

	# monotonically increasing genes/ restoration genes
	temp = ((pval<pv) & (cor>=co))
	genes = r2.index[temp]

	sig = r2.loc[temp,:]
	sig['spcor'] = cor[temp]
	sig['pval'] = pval[temp]
	print(sig.shape)
	# print(sig.head())
	# save restoration genes
	sig_r=sig
	sig.to_csv(path["sigi"])"""

def r2_feature_wise(path, vlm, feature="leiden", m="mis"):
        """ returns a numpy array of R-squared value for each gene feature wise"""
        uni = np.sort(np.unique(vlm.ca[feature]))
        dim2 = uni.shape[0]
        r2f = np.zeros(shape=(vlm.S.shape[0],dim2))
        for i in range(dim2):
            x = uni[i]
            samples = (vlm.ca[feature]==x)
            for j in range(vlm.S.shape[0]):
                if m=="mis":
                    r2f[j,i] = mutual_info_score(labels_true=vlm.Ux_sz[j,samples], labels_pred=vlm.Upred[j,samples])
                elif m=="r2":
                    r2f[j,i] = r2_score(y_true=vlm.Ux_sz[j,samples], y_pred=vlm.Upred[j,samples])
                else:
                    print("m can be either r2 ")
        # save r2 matrix in csv format
        leidens = np.unique(vlm.ca['leiden'])
        r2df = pd.DataFrame(r2f, index=vlm.ra['var_names'], columns=leidens)
        r2df.to_csv(path['r2'])
        print(r2df.shape)
        r2df.head()
        return r2df

def fitting_gamma(adata,path):
	bdata = scp.read_loom(path["path"], sparse=True, X_name='spliced')
	bdata=bdata[adata.obs.index,]
	bdata.obs['leiden']=adata.obs['leiden']
	bdata.write_loom(path['loom'])
	vlm = vcy.VelocytoLoom(path["loom"])
	# gene filtering 
	vlm.score_detection_levels(min_cells_express=20, min_expr_counts=50)
	vlm.filter_genes(by_detection_levels=True)
	vlm.score_detection_levels(min_expr_counts=0, min_cells_express=0, min_expr_counts_U=25, min_cells_express_U=20)
	vlm.filter_genes(by_detection_levels=True)
	# print(vlm.S.shape)

	# size normalization
	vlm._normalize_S(relative_size=vlm.initial_cell_size, target_size=np.median(vlm.initial_cell_size))
	vlm._normalize_U(relative_size=vlm.initial_Ucell_size, target_size=np.median(vlm.initial_Ucell_size))

	# PCA
	vlm.perform_PCA()
	pcn = vlm.S.shape[0]
	# plt.plot(np.cumsum(vlm.pca.explained_variance_ratio_)[:100])
	n_comps = np.where(np.diff(np.diff(np.cumsum(vlm.pca.explained_variance_ratio_))>0.002))[0][0]
	plt.axvline(n_comps, c="k")
	print("n_comps", n_comps)

	# KNN smoothing
	k = int(vlm.S.shape[1]*0.025)
	print("k",k)
	vlm.knn_imputation(n_pca_dims=n_comps, k=k, balanced=True, b_sight=k*8, b_maxl=k*4, n_jobs=16)

	# fit gamma
	vlm.fit_gammas()

	# estimate velocity
	vlm.predict_U()
	vlm.calculate_velocity()
	vlm.calculate_shift(assumption="constant_velocity")
	vlm.extrapolate_cell_at_t(delta_t=1.,)
	print("velocity Done!")
	return vlm

def clustering(adata, min_genes, min_cells, n_genes_by_counts, pct_counts_mt, resolution):
	scp.settings.verbosity = 3
	scp.logging.print_header()
	scp.settings.set_figure_params(dpi=80, facecolor='white')
	print(adata)
	# print(type(adata))
	adata.var_names_make_unique()
	scp.pp.filter_cells(adata, min_genes=200)
	scp.pp.filter_genes(adata, min_cells=3) 
	adata.var['mt'] = adata.var_names.str.startswith('MT-')
	scp.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)
	# scp.pl.violin(adata, ['n_genes_by_counts', 'total_counts'],jitter=0.4, multi_panel=True)
	# scp.pl.scatter(adata, x='total_counts', y='n_genes_by_counts')
	adata = adata[adata.obs.n_genes_by_counts < 2500, :]
	adata = adata[adata.obs.pct_counts_mt < 5, :]
	adata.obs['CellID'] = adata.obs.index
	adata.var['Gene'] = adata.var.index
	# normalize
	scp.pp.normalize_total(adata, target_sum=1e4)
	# log transform
	scp.pp.log1p(adata)
	# highly variable genes
	scp.pp.highly_variable_genes(adata, n_top_genes=2000)
	adata = adata[:, adata.var.highly_variable]
	scp.pp.regress_out(adata, ['total_counts', 'pct_counts_mt'])
	scp.pp.scale(adata, max_value=10)
	scp.tl.pca(adata, svd_solver='arpack')
	# scp.pl.pca(adata)
	# scp.pl.pca_variance_ratio(adata, log=True)
	scp.pp.neighbors(adata, n_neighbors=10, n_pcs=40)
	scp.tl.umap(adata)
	scp.tl.leiden(adata,resolution=resolution)
	scp.pl.umap(adata, color=['leiden'])
	return adata

def HDS(path1=None, clusters=None, genes=None, per=.1,
# pv=0.025, co=.9, r_c=0, 
min_genes=200, min_cells=3, n_genes_by_counts=2500, pct_counts_mt=5, resolution=1):
    # path variables
    path = {}
    path['path']=path1
    root = os.getcwd()+'/'+'loom_data'
    if not os.path.exists(os.getcwd()+'/'+'loom_data'):
      os.mkdir(root)
    adata = scp.read_loom(path['path'], sparse=False, X_name='spliced')
    if not clusters:
      adata=clustering(adata, min_genes, min_cells, n_genes_by_counts,pct_counts_mt, resolution)
    else:
      adata.obs['leiden']=clusters
    path["loom"] = root+ "/temp.loom"
    path["metadata"] = root+"/metadata.csv"
    path["sigi"] = root+"/significant_restoration_genes_across_all_cells.csv"
    path["sigd"] = root+"/significant_hb_genes_across_all_cells.csv"
    path['r2'] = root+"/r2_all_cells.csv"
    path["velocity_age_0p025"] = root+"/Velocity_0p025_age_specific_gamma.csv"
    # plots save location
    path['save'] = root+"/"
    # fitting gamma
    vlm=fitting_gamma(adata,path)
    # compute r-squared leiden wise
    leiden = np.unique(vlm.ca['leiden'])
    r2 = r2_feature_wise(path, vlm, feature='leiden',m="r2")
    # mis = r2_feature_wise(path, vlm, feature='leiden',m="mis")
    violin_plotting(path,r2,per=per)
    # getting_cor(r2,pv=0.025,co=.9)
    # r2_cut(path, r_c, r2)
    # count_genes()
    # sigi = pd.read_csv(path["sigi"], index_col=0)
    # sigd = pd.read_csv(path["sigd"], index_col=0)
    if genes:
      genes=np.intersect1d(genes,r2.index)
      if len(genes)>0:
      		plot_genes_r2_phase_portrait_supp_hb(path, vlm, r2, genes, figname=True)
      else:
            print("no common gene found!")
    else:
      genes=r2.index[:5]
      plot_genes_r2_phase_portrait_supp_hb(path, vlm, r2, genes, figname=True)
      """genes=sigi.index[:5]
      plot_genes_r2_phase_portrait_supp_hb(path, vlm, sigi, genes, figname=True)
      genes=sigd.index[:5]
      plot_genes_r2_phase_portrait_supp_hb(path, vlm, sigd, genes, figname=True)"""
    return r2
