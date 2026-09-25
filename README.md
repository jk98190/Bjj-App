# BJJ Progression Tracker & Study Bank

An interactive, Python-powered dashboard built on **Jupyter Notebook**, **Voila**, and **Pandas** to track mat hours, analyze training metrics, and master reaction-based grappling decision trees.

---

## Key Features

* **Session Logger:** Track training volume, rank progression (Belt/Stripes), session styles (Gi, No-Gi, Wrestling), total sparring rounds, submissions given/received, and workout notes.
* **Technique & Match Breakdown Bank:** Interactive card system equipped with embedded YouTube study videos, position tags, and step-by-step mechanical breakdowns.
* **System Decision Trees:** Visual ASCII pathways mapping out high-level grappling frameworks:
  * **Adele Fornarino's Kimura Chain** (*Armbar ➔ Triangle ➔ Omoplata decision tree*)[cite: 1]
  * **Half Guard Rescue & Clamp System** (*Knee Lever vs. Windmill Bridge escapes*)[cite: 1]
  * **GSP Level-Change Wrestling Entries** (*Double leg corner-turning & single-leg collections*)[cite: 1]
* **Analytics Dashboard:** Automatically computes total mat hours, round volume, and renders interactive monthly training volume charts powered by Plotly.

---

##  Tech Stack

* **Language:** Python 3.9+
* **UI/Interface:** `ipywidgets`, `IPython.display`
* **Data Processing:** `pandas`
* **Data Visualization:** `plotly`
* **Web App Rendering:** `voila`

---

## Quick Start Guide

### 1. Prerequisites & Installation

Clone the repository and install the required dependencies:

```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/bjj-tracker-app.git](https://github.com/YOUR_USERNAME/bjj-tracker-app.git)
cd bjj-tracker-app

# Install dependencies
pip install pandas plotly ipywidgets voila
