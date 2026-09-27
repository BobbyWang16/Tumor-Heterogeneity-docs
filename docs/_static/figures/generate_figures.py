"""Reproduce website illustrations using synthetic arrays only.

Run: python docs/_static/figures/generate_figures.py
Requires numpy, scipy and matplotlib. No implementation package or patient data.
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import ListedColormap
from scipy.ndimage import gaussian_filter, uniform_filter, distance_transform_edt

OUT = Path(__file__).resolve().parent
SEED = 42
rng = np.random.default_rng(SEED)
y, x = np.mgrid[:128, :128]
roi = ((x - 64) / 38) ** 2 + ((y - 64) / 43) ** 2 <= 1
n = roi.sum()
noise = rng.normal(size=n)
noise = (noise - noise.mean()) / noise.std()
low, high = np.full(roi.shape, np.nan), np.full(roi.shape, np.nan)
low[roi], high[roi] = 60 + 4 * noise, 60 + 22 * noise
field = gaussian_filter(rng.normal(size=roi.shape), 8)
values = np.sort(high[roi])
ordered = np.empty(n)
ordered[np.argsort(field[roi])] = values
clustered, mixed = high.copy(), high.copy()
clustered[roi] = ordered
mixed[roi] = rng.permutation(values)
assert np.array_equal(np.sort(clustered[roi]), np.sort(mixed[roi]))
assert np.isclose(low[roi].mean(), high[roi].mean())

plt.rcParams.update({'font.size': 12, 'axes.titlesize': 13,
    'axes.spines.top': False, 'axes.spines.right': False,
    'svg.fonttype': 'none', 'pdf.fonttype': 42, 'axes.titlepad': 14})

def save(fig, name, lang, title):
    fig.suptitle(title, fontsize=18, fontweight='bold', color='#163b4c')
    fig.text(.02, .015, '模拟数据 · 教学示意 · 非患者影像' if lang == 'zh' else
             'SYNTHETIC DATA · EDUCATIONAL ILLUSTRATION · NOT PATIENT IMAGING',
             fontsize=10, color='#52636a')
    fig.savefig(OUT / f'{name}-{lang}.png', dpi=180, facecolor='white')
    fig.savefig(OUT / f'{name}-{lang}.svg', facecolor='white')
    plt.close(fig)

def image(ax, data, title, cmap='cividis', vmin=0, vmax=120):
    im = ax.imshow(np.ma.masked_invalid(data), cmap=cmap, vmin=vmin, vmax=vmax,
                   interpolation='nearest')
    ax.set_title(title, loc='left')
    ax.set_axis_off()
    return im

def local_sd(a):
    a = np.where(roi, a, 0)
    w = uniform_filter(roi.astype(float), 9)
    mean = uniform_filter(a, 9) / np.maximum(w, 1e-12)
    var = uniform_filter(a*a, 9) / np.maximum(w, 1e-12) - mean*mean
    return np.where(roi, np.sqrt(np.maximum(var, 0)), np.nan)

with (OUT/'summary.csv').open('w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['synthetic_case', 'roi_pixels', 'mean', 'population_sd'])
    for name, a in [('narrow',low), ('wide',high), ('clustered',clustered), ('mixed',mixed)]:
        writer.writerow([name,int(n),float(a[roi].mean()),float(a[roi].std())])

for lang in ('zh', 'en'):
    zh = lang == 'zh'
    if zh:
        font_manager.findfont('Microsoft YaHei', fallback_to_default=False)
    plt.rcParams['font.family'] = 'Microsoft YaHei' if zh else 'DejaVu Sans'
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.8), gridspec_kw={'width_ratios':[1,1,1.35]})
    fig.subplots_adjust(left=.025, right=.98, top=.76, bottom=.22, wspace=.3)
    im = image(axes[0],low,'a  较窄灰度分布' if zh else 'a  Narrow distribution')
    image(axes[1],high,'b  较宽灰度分布' if zh else 'b  Wide distribution')
    for ax, sd in zip(axes[:2], [4,22]):
        ax.text(.5,-.06, f'均值 60 · 标准差 {sd}' if zh else f'Mean 60 · SD {sd}',
                transform=ax.transAxes,ha='center',fontsize=11)
    cb=fig.colorbar(im,ax=axes[:2],orientation='horizontal',fraction=.05,pad=.18,aspect=38)
    cb.set_label('模拟灰度（任意单位）' if zh else 'Synthetic intensity (a.u.)',fontsize=10)
    bins=np.linspace(-30,150,46)
    for a, c, label in [(low,'#137f88','较窄' if zh else 'Narrow'),(high,'#be6a32','较宽' if zh else 'Wide')]:
        axes[2].hist(a[roi],bins=bins,density=True,histtype='step',lw=2,color=c,label=label)
    axes[2].set(title='c  分布对比' if zh else 'c  Compare distributions',
                xlabel='模拟灰度' if zh else 'Synthetic intensity',ylabel='概率密度' if zh else 'Density')
    axes[2].legend(fontsize=10)
    save(fig,'intensity',lang,'均值相同，内部差异可以不同' if zh else 'The same mean can hide different variability')

    fig, axes=plt.subplots(2,2,figsize=(10,8))
    fig.subplots_adjust(left=.06,right=.84,top=.85,bottom=.09,hspace=.28,wspace=.12)
    for ax,a,title in zip(axes[0],[clustered,mixed],
         ['a  成片排列','b  打散排列'] if zh else ['a  Clustered arrangement','b  Shuffled arrangement']):
        im=image(ax,a,title)
    cb=fig.colorbar(im,cax=fig.add_axes([.87,.57,.02,.23]))
    cb.set_label('模拟灰度' if zh else 'Synthetic intensity')
    for ax,a,title in zip(axes[1],[clustered,mixed],
         ['c  局部变化较平缓','d  局部变化较剧烈'] if zh else ['c  Smoother local variation','d  Stronger local variation']):
        im=image(ax,local_sd(a),title,'magma',0,30)
    cb=fig.colorbar(im,cax=fig.add_axes([.87,.13,.02,.23]))
    cb.set_label('9 × 9 邻域标准差' if zh else '9 × 9 local SD')
    save(fig,'spatial',lang,'灰度值完全相同，空间排列依然重要' if zh else 'Identical intensity values, different spatial organization')

    background=-700+40*gaussian_filter(rng.normal(size=roi.shape),3)
    background[roi]=clustered[roi]
    labels=np.where(roi,np.digitize(clustered,[50,70])+1,np.nan)
    ring=(distance_transform_edt(~roi)<=10)&~roi
    fig,axes=plt.subplots(1,4,figsize=(14,4.7))
    fig.subplots_adjust(left=.02,right=.98,top=.76,bottom=.2,wspace=.15)
    image(axes[0],background,'a  模拟影像' if zh else 'a  Synthetic image','gray',-800,120)
    image(axes[1],background,'b  肿瘤区域' if zh else 'b  Tumor region','gray',-800,120)
    axes[1].contour(roi,levels=[.5],colors=['#23c6bc'],linewidths=2)
    image(axes[2],labels,'c  示意性分区' if zh else 'c  Illustrative regions',
          ListedColormap(['#315b91','#29a99a','#edb550']),1,3)
    image(axes[3],background,'d  瘤周区域' if zh else 'd  Surrounding region','gray',-800,120)
    axes[3].imshow(np.ma.masked_where(~ring,ring),cmap=ListedColormap(['#edb550']),alpha=.8,interpolation='nearest')
    subtitles=['统一窗宽显示','青色轮廓：分析范围','阈值分区，非模型预测','金色环带：10 像素'] if zh else ['Shared display window','Teal contour: analysis ROI','Thresholds, not predictions','Gold ring: 10 pixels']
    for ax,label in zip(axes,subtitles):
        ax.text(.5,-.07,label,transform=ax.transAxes,ha='center',fontsize=11)
    save(fig,'workflow',lang,'从影像到区域：如何阅读空间图' if zh else 'From image to regions: reading spatial maps')
print('Generated six bilingual PNG/SVG figures and summary.csv')
