"""Python-only, synthetic teaching diagrams for the design-principles pages.

Contract: explain each algorithm's information flow, not demonstrate performance.
Archetype: schematic-led composites. Export: 13 x 4 inch PNG and editable SVG.
No patient data, fitted models, significance tests or clinical claims.
Requires numpy, scipy, matplotlib; Chinese labels require Microsoft YaHei.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.colors import ListedColormap
from scipy.spatial import ConvexHull

OUT=Path(__file__).resolve().parent
plt.rcParams.update({'svg.fonttype':'none','font.size':12,'axes.titlesize':13})
rng=np.random.default_rng(8)
y,x=np.mgrid[-1:1:100j,-1:1:100j]
mask=x*x+y*y<.75**2
signal=60+22*np.sin(6*x)*np.cos(5*y)
regions=np.digitize(signal,[50,70]).astype(float)
cmap=ListedColormap(['#315b91','#23a699','#edb550'])

def save(fig,name,lang):
    fig.text(.025,.03,'教学示意 · 模拟数组 / 手绘结构 · 不是算法运行结果' if lang=='zh' else
             'TEACHING SCHEMATIC · SYNTHETIC ARRAYS / HAND-DRAWN STRUCTURES · NOT MODEL OUTPUT',fontsize=9,color='#52636a')
    fig.savefig(OUT/f'design-{name}-{lang}.png',dpi=160,facecolor='white')
    fig.savefig(OUT/f'design-{name}-{lang}.svg',facecolor='white')
    plt.close(fig)

def flow(name,title,steps,lang):
    fig,ax=plt.subplots(figsize=(13,3.4)); ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    fig.suptitle(title,color='#163b4c',fontsize=19,fontweight='bold',y=.94)
    n=len(steps);w=.86/n
    for i,(head,body) in enumerate(steps):
        left=.025+i*.97/n
        ax.add_patch(FancyBboxPatch((left,.25),w,.5,boxstyle='round,pad=.012',fc='#eef6f6',ec='#a7c6c7'))
        ax.text(left+w/2,.62,head,ha='center',va='center',weight='bold',color='#137f88',fontsize=14)
        ax.text(left+w/2,.43,body,ha='center',va='center',fontsize=12,linespacing=1.6)
        if i<n-1: ax.annotate('',(left+w+.055,.5),(left+w+.015,.5),arrowprops={'arrowstyle':'->','color':'#137f88','lw':2})
    save(fig,name,lang)

models={
'dhi':(['DHI：从分布到相对变异','ROI 内灰度','分位数保留','样本标准差 / 均值'],['DHI: from distribution to relative variation','ROI intensities','Percentile selection','Sample SD / mean']),
'bih':(['BIH：观察尺度如何改变信号摘要','最大轴向切面','改变盒尺度','对数拟合 → 负斜率'],['BIH: signal summaries across scales','Largest axial slice','Change box size','Log fit → negative slope']),
'hab':(['HAB：区域组成与空间排列共同描述','灰度 + 空间先验','GMM 图像生境','多项描述 → 固定权重'],['HAB: composition and arrangement','Intensity + spatial priors','GMM image habitats','Descriptors → fixed weights']),
'thi':(['THI：关注同类区域是否碎片化','局部纹理特征','KMeans 纹理类别','最大连通块比例'],['THI: fragmentation within each class','Local texture features','KMeans texture classes','Largest-component fraction']),
'pth':(['PTH：比较肿瘤周围的组织块','保留瘤周组织','环带内 SLIC 分块','块间特征变异'],['PTH: compare tissue around the tumor','Retain surrounding tissue','SLIC blocks in a ring','Across-block variability']),
'shi':(['SHI：从三维掩膜描述形态','三维肿瘤掩膜','表面与凸包','多个几何描述'],['SHI: describe 3D mask geometry','3D tumor mask','Surface and convex hull','Geometric descriptors']),
'ith-fs':(['ITH-FS：在关系图上联合特征与空间','多尺度体素特征','相似 + 相近 → 图','谱聚类 → 分区'],['ITH-FS: joint feature and spatial relations','Multi-scale voxel features','Similarity + proximity → graph','Spectral clustering → regions'])}

def show(ax,a,colors='cividis'):
    ax.imshow(np.ma.masked_where(~mask,a),cmap=colors,interpolation='nearest');ax.axis('off')

for lang in ['zh','en']:
    zh=lang=='zh';plt.rcParams['font.family']='Microsoft YaHei' if zh else 'DejaVu Sans'
    for key,labels in models.items():
        t=labels[0 if zh else 1]
        fig,axes=plt.subplots(1,3,figsize=(13,4.3));fig.subplots_adjust(top=.73,bottom=.2,wspace=.32,left=.05,right=.95)
        fig.suptitle(t[0],fontsize=18,color='#163b4c',weight='bold',y=.96)
        for i,ax in enumerate(axes):ax.set_title(f'{i+1}  {t[i+1]}',pad=12)
        if key=='dhi':
            show(axes[0],signal)
            vals=signal[mask];lo,hi=np.percentile(vals,[5,95])
            axes[1].hist(vals,bins=22,color='#93c9c9');axes[1].axvspan(lo,hi,alpha=.2,color='#137f88');axes[1].set_xlabel('5–95% ' + ('仅为示例' if zh else 'illustration only'));axes[1].set_yticks([])
            axes[2].axis('off');axes[2].text(.5,.6,r'$CV=\frac{s}{\bar{x}+\epsilon}$',ha='center',fontsize=30);axes[2].text(.5,.25,'均值接近 0 时需谨慎' if zh else 'Inspect near-zero means',ha='center',fontsize=13)
        elif key=='bih':
            show(axes[0],signal);show(axes[1],signal)
            for k in range(0,100,20):axes[1].axvline(k,color='white',lw=.8);axes[1].axhline(k,color='white',lw=.8)
            axes[1].text(.5,-.1,'网格仅示意一个尺度' if zh else 'One illustrative grid scale',transform=axes[1].transAxes,ha='center',fontsize=10)
            axes[2].axis('off');axes[2].text(.5,.55,'log(scale) → log(signal)\n\nfd = −slope',ha='center',va='center',fontsize=17);axes[2].text(.5,.1,'检查 r² 与残差' if zh else 'Inspect r² and residuals',ha='center',fontsize=12)
        elif key in ['hab','thi','ith-fs']:
            show(axes[0],signal)
            if key=='ith-fs':
                pos=np.array([[.2,.2],[.25,.65],[.5,.45],[.75,.75],[.8,.25]])
                for a,b in [(0,1),(0,2),(1,2),(2,3),(2,4),(3,4)]:axes[1].plot(*pos[[a,b]].T,color='#9ab9bf',lw=2)
                axes[1].scatter(*pos.T,s=170,color=['#315b91']*3+['#edb550']*2);axes[1].set(xlim=(0,1),ylim=(0,1));axes[1].axis('off');show(axes[2],regions,cmap)
            else:
                show(axes[1],regions,cmap);axes[2].axis('off')
                text=('组成 / 分层 / 混合 / 碎片\n↓\n加权并裁剪到 [0, 1]' if zh else 'Composition / layering / mixing\n+ fragmentation\n↓ weighted sum, clip to [0, 1]') if key=='hab' else ('每类：最大块 / 该类总体积\n↓ 类别均值\nTHI = 1 − 均值' if zh else 'Per class: largest / total volume\n↓ average across classes\nTHI = 1 − average')
                axes[2].text(.5,.5,text,ha='center',va='center',fontsize=14,linespacing=1.7)
        elif key=='pth':
            radius=np.sqrt(x*x+y*y);ring=(radius>.75)&(radius<.95)
            for ax in axes[:2]:
                ax.imshow(np.where(mask,.4,np.nan),cmap='gray',vmin=0,vmax=1);ax.axis('off')
            axes[0].imshow(np.ma.masked_where(~ring,ring),cmap=ListedColormap(['#edb550']))
            blocks=np.floor((np.arctan2(y,x)+np.pi)*6/np.pi)%6
            axes[1].imshow(np.ma.masked_where(~ring,blocks),cmap=ListedColormap(['#315b91','#5292bc','#23a699','#a9d5b9','#edb550','#c88850']))
            axes[1].text(.5,-.1,'扇区仅示意，非 SLIC 输出' if zh else 'Sectors illustrate blocks, not SLIC output',transform=axes[1].transAxes,ha='center',fontsize=9)
            axes[2].axis('off');axes[2].text(.5,.5,'mean(PTH_CV_*)',ha='center',fontsize=20)
        else:
            for i,ax in enumerate(axes[:2]):
                theta=np.linspace(0,2*np.pi,200);r=.7+.09*np.cos(5*theta)
                ax.fill(r*np.cos(theta),r*np.sin(theta),color='#a7cdcf');ax.set_aspect('equal');ax.axis('off')
                if i:
                    pts=np.c_[r*np.cos(theta),r*np.sin(theta)]
                    hull=ConvexHull(pts); hp=pts[np.r_[hull.vertices,hull.vertices[0]]]
                    ax.plot(hp[:,0],hp[:,1],color='#c88850',ls='--',lw=2)
                ax.text(.5,-.1,'二维轮廓示意三维几何' if zh else '2D sketch of 3D geometry',transform=ax.transAxes,ha='center',fontsize=10)
            axes[2].axis('off');axes[2].text(.5,.5,'1 − sphericity\n1 − solidity\nFD_surface / 3\n↓\n' + ('可用项均值' if zh else 'Mean of available terms'),ha='center',va='center',fontsize=15)
        save(fig,key,lang)
    flow('interface','共享入口，保留不同输出' if zh else 'Shared input, distinct outputs',
         [('输入','image + mask'),('模型','compute(image, mask)'),('输出','score + features\n' + ('可选空间图' if zh else 'optional maps'))] if zh else [('Input','image + mask'),('Model','compute(image, mask)'),('Output','score + features\noptional maps')],lang)
    flow('inspection','从检查到解释' if zh else 'Inspect before interpreting',
         [('输入','对齐 / 掩膜 / 参数'),('质量','失败记录 / 拟合质量'),('解释','特征 + 空间图'),('比较','病例与队列差异')] if zh else [('Input','Alignment / mask / settings'),('Quality','Failures / fit quality'),('Interpret','Features + spatial maps'),('Compare','Cases and cohorts')],lang)
    fig,ax=plt.subplots(figsize=(13,4));fig.subplots_adjust(top=.8,bottom=.22);ax.axis('off');ax.set(xlim=(0,18),ylim=(0,3))
    fig.suptitle('5 个体素，不一定是同样的距离' if zh else 'Five voxels need not mean the same distance',fontsize=19,color='#163b4c',weight='bold')
    for row,size in [(2,1),(.5,3)]:
        for k in range(5):ax.add_patch(plt.Rectangle((1+k*size,row),size,.55,fc='#a7cdcf',ec='white',lw=2))
        ax.text(1,row+.75,f'5 × {size} mm = {5*size} mm',fontsize=16,color='#137f88')
    save(fig,'spacing',lang)
print('Exported 10 diagram pairs')
