from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
DATA = ROOT / 'data'
ASSETS.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)

# Formal baseline data verified in the experiment
baseline = pd.DataFrame({
    'Trial': list(range(1, 11)),
    'T1_ms': [101, 102, 101, 102, 101, 101, 102, 94, 101, 94],
    'T2_ms': [156] * 10,
    'Peak_Z': [544.24, 544.24, 544.24, 544.24, 544.24, 544.24, 544.24, 544.97, 544.24, 544.97],
    'Sound': ['No','No','No','No','No','No','No','Yes','No','Yes'],
})
baseline.to_csv(DATA / 'baseline_verified_trials.csv', index=False)

# Figure 1: timing diagram
fig, ax = plt.subplots(figsize=(12, 5.5))
ax.set_xlim(0, 12); ax.set_ylim(0, 7); ax.axis('off')
y = 5.6
ax.annotate('', xy=(11.5, y), xytext=(0.8, y), arrowprops=dict(arrowstyle='->', lw=1.5))
ax.text(11.6, y, 'Time (ms)', va='center', fontsize=11)
x_crouch, x_space, x_release, x_takeoff = 1.8, 4.2, 6.7, 9.8
for x, label in [(x_crouch,'Press Crouch'),(x_space,'Press Space'),(x_release,'Release Space'),(x_takeoff,'Takeoff')]:
    ax.plot([x,x],[5.15,6.05], ls='--', lw=1)
    ax.text(x, 6.15, label, ha='center', fontsize=10)
ax.add_patch(plt.Rectangle((x_crouch,4.55), x_space-x_crouch, 0.35, alpha=.35))
ax.text(0.2, 4.72, 'Crouch', fontsize=11, va='center')
ax.add_patch(plt.Rectangle((x_space,3.85), x_release-x_space, 0.35, alpha=.35))
ax.text(0.2, 4.02, 'Jump / Space', fontsize=11, va='center')
ax.annotate('', xy=(x_space,5.0), xytext=(x_crouch,5.0), arrowprops=dict(arrowstyle='<->', lw=1.8))
ax.text((x_crouch+x_space)/2,5.12,'T1',ha='center',fontweight='bold',fontsize=12)
ax.annotate('', xy=(x_release,3.55), xytext=(x_space,3.55), arrowprops=dict(arrowstyle='<->', lw=1.8))
ax.text((x_space+x_release)/2,3.67,'H',ha='center',fontweight='bold',fontsize=12)
ax.annotate('', xy=(x_takeoff,5.0), xytext=(x_release,5.0), arrowprops=dict(arrowstyle='<->', lw=1.8))
ax.text((x_release+x_takeoff)/2,5.12,'T2',ha='center',fontweight='bold',fontsize=12)
xs = [7.1, 7.8, 8.6, 9.4, 10.2, 11.0]
zs = [1.2, 1.7, 2.6, 3.1, 2.0, 1.25]
ax.plot(xs, zs, lw=2)
ax.scatter([xs[3]],[zs[3]], s=35)
ax.text(xs[3], zs[3]+0.25, 'Peak Z', ha='center', fontsize=10)
ax.text(0.2,1.25,'Vertical position (Z)',fontsize=11)
ax.text(0.2,0.55,'Schematic only — not an actual gameplay frame.',fontsize=9)
ax.set_title('Figure 1. Input Timing and Key Variable Diagram', loc='left', fontweight='bold')
fig.tight_layout(); fig.savefig(ASSETS/'input-timing-diagram.png', dpi=200, bbox_inches='tight'); plt.close(fig)

# Unnumbered workflow diagram: VRF -> vrfkit -> analysis
fig, ax = plt.subplots(figsize=(13, 4.2))
ax.set_xlim(0, 13); ax.set_ylim(0, 4.2); ax.axis('off')
boxes = [
    (0.4, 1.35, 2.0, 1.15, 'VALORANT replay\n.vrf'),
    (3.0, 1.35, 2.0, 1.15, 'vrfkit\nreplay parser'),
    (5.6, 0.65, 2.6, 2.55, 'Parsed outputs\n\nmovement.parquet\nfields.parquet\nactors.parquet\nmanifest.json'),
    (8.85, 1.35, 1.7, 1.15, 'Trial / event\nalignment'),
    (11.15, 1.35, 1.45, 1.15, 'Analysis &\nfigures'),
]
for x, y0, w, h, text in boxes:
    ax.add_patch(FancyBboxPatch((x,y0), w,h, boxstyle='round,pad=0.04', fill=False, lw=1.5))
    ax.text(x+w/2, y0+h/2, text, ha='center', va='center', fontsize=10)
for x1, x2 in [(2.4,3.0),(5.0,5.6),(8.2,8.85),(10.55,11.15)]:
    ax.annotate('', xy=(x2,1.93), xytext=(x1,1.93), arrowprops=dict(arrowstyle='->', lw=1.5))
ax.set_title('Replay Data Processing Workflow', loc='left', fontweight='bold')
ax.text(0.4,0.2,'vrfkit converts the .vrf replay into structured tables used for timing and movement analysis.', fontsize=9)
fig.tight_layout(); fig.savefig(ASSETS/'replay-processing-workflow.png', dpi=200, bbox_inches='tight'); plt.close(fig)

# Figure 2: Space hold duration comparison
hold = pd.DataFrame({
    'H_nominal_ms': [20, 300, 20, 300],
    'Vertical_displacement': [115.00, 115.00, 109.32, 109.32],
    'Condition': ['Normal jump', 'Normal jump', 'Crouch condition', 'Crouch condition'],
})
fig, ax = plt.subplots(figsize=(7.5,5))
for label, grp in hold.groupby('Condition'):
    ax.plot(grp['H_nominal_ms'], grp['Vertical_displacement'], marker='o', linewidth=2, label=label)
ax.set_xlabel('Nominal Space hold duration H (ms)')
ax.set_ylabel('Vertical displacement')
ax.set_title('Figure 2. Space Hold Duration vs Vertical Displacement')
ax.grid(True, alpha=.3); ax.legend(); fig.tight_layout()
fig.savefig(ASSETS/'space-hold-comparison.png', dpi=200); plt.close(fig)

# Figure 3: T1 vs T2
fig, ax = plt.subplots(figsize=(7,5))
for label, grp in baseline.groupby('Sound'):
    ax.scatter(grp['T1_ms'], grp['T2_ms'], s=100, label=f'Sound: {label}')
for _, r in baseline.iterrows():
    ax.annotate(str(int(r['Trial'])), (r['T1_ms'], r['T2_ms']), xytext=(5,5), textcoords='offset points', fontsize=8)
ax.set_xlabel('T1 (ms)'); ax.set_ylabel('T2 (ms)')
ax.set_title('Figure 3. Formal Baseline: T1 vs T2')
ax.grid(True, alpha=.3); ax.legend(); fig.tight_layout()
fig.savefig(ASSETS/'t1-t2-scatter.png', dpi=200); plt.close(fig)

# Figure 4: trial order vs T1/T2
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(baseline['Trial'], baseline['T1_ms'], marker='o', label='T1')
ax.plot(baseline['Trial'], baseline['T2_ms'], marker='o', label='T2')
for _, r in baseline.iterrows():
    ax.annotate('Y' if r['Sound']=='Yes' else 'N', (r['Trial'], r['T1_ms']), xytext=(0,8), textcoords='offset points', ha='center', fontsize=8)
ax.set_xlabel('Trial'); ax.set_ylabel('Time (ms)'); ax.set_xticks(baseline['Trial'])
ax.set_title('Figure 4. Trial Order vs T1 and T2')
ax.grid(True, alpha=.3); ax.legend(); fig.tight_layout()
fig.savefig(ASSETS/'trial-order-t1-t2.png', dpi=200); plt.close(fig)

# Figure 5: T1 vs Peak Z
fig, ax = plt.subplots(figsize=(7,5))
for label, grp in baseline.groupby('Sound'):
    ax.scatter(grp['T1_ms'], grp['Peak_Z'], s=100, label=f'Sound: {label}')
for _, r in baseline.iterrows():
    ax.annotate(str(int(r['Trial'])), (r['T1_ms'], r['Peak_Z']), xytext=(5,5), textcoords='offset points', fontsize=8)
ax.set_xlabel('T1 (ms)'); ax.set_ylabel('Peak Z')
ax.set_title('Figure 5. T1 vs Peak Z')
ax.grid(True, alpha=.3); ax.legend(); fig.tight_layout()
fig.savefig(ASSETS/'t1-vs-peak-z.png', dpi=200); plt.close(fig)

# Figure 6: observed state summary, including A condition
states = pd.DataFrame({
    'T1_ms': [86, 94, 101.5],
    'Peak_Z': [545.70, 544.97, 544.24],
    'Crouch_depth': [6.25, 6.82, 7.39],
    'Sound': ['Audible', 'Audible', 'Silent'],
    'State': ['A condition', 'Baseline audible', 'Baseline silent'],
})
fig, ax = plt.subplots(figsize=(8,5.5))
for sound, grp in states.groupby('Sound'):
    ax.scatter(grp['T1_ms'], grp['Peak_Z'], s=150, label=sound)
for _, r in states.iterrows():
    ax.annotate(f"{r['State']}\nCrouch depth ≈ {r['Crouch_depth']}", (r['T1_ms'], r['Peak_Z']), xytext=(8,8), textcoords='offset points', fontsize=9)
ax.set_xlabel('Observed T1 (ms)'); ax.set_ylabel('Peak Z')
ax.set_title('Figure 6. Observed Timing / Movement State Levels')
ax.grid(True, alpha=.3); ax.legend(); fig.tight_layout()
fig.savefig(ASSETS/'observed-state-levels.png', dpi=200); plt.close(fig)

print('Generated figures, workflow diagram, and baseline CSV.')
