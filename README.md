# Building Refrigeration System

## 🧊 About

The existing refrigeration system for OpenStudio was originally designed for a prototype supermarket model. To support the development of new modular space types, it is crucial to refactor the system. This process includes refining the design by utilizing the manufacturer's existing data, along with incorporating the latest data from manufacturers, to enhance the system’s adaptability and functionality.

This repository currently contains the refrigeration system database and Python-based automation for generating OpenStudio-compatible refrigeration JSON files.

**This is a work in progress.**

---

## 📁 Project Structure

- **`main.ipynb`**: Primary execution file to run the full modeling and export workflow.
- **`example_automated_mode.ipynb`**: Example file demonstrating **automated** mode with default SuperMarket configuration.
- **`example_user_mode.ipynb`**: Example file for **manual mode**, allowing user-defined configuration of refrigeration systems.

---

## 🧰 OpenStudio Refrigeration System Modeling and JSON Generator

### Step-by-Step Guide

This notebook provides a structured workflow to generate and export OpenStudio-compatible JSON files for supermarket refrigeration systems.

#### 🔑 Key modules:
- Compressor and performance curve generation  
- Condenser and fan curve logic  
- Rack assignment based on thermal loads  
- Case and Walk-in object creation  
- Full refrigeration system assembly and export  

---

## 🌍 Practical Applications

This framework can be applied to multiple real-world use cases:

### 🔧 Practical Refrigeration Design
Engineers and energy consultants can use the generated components to design and evaluate supermarket refrigeration systems under different templates (`old`, `new`, `advanced`).

### 🏗️ OpenStudio Energy Modeling
The JSON objects generated here follow OpenStudio's **v0.2.1** schema, allowing seamless integration with building simulation models for:

- Load estimation  
- Retrofit analysis  
- Performance benchmarking  

This tool bridges **design-level thinking** and **simulation-level precision** by linking real data to automated JSON object creation.

---

## ⚙️ Mode Selection: How to Start

The modeling framework provides two modes of operation:

### ✅ Automated Mode
Automatically configures a predefined SuperMarket setup including:
- Case/Walk-in units
- Rack assignments
- Refrigerant templates  

→ **Ideal for quick simulations and standard scenarios**

### 🎛️ User-Defined Mode
Lets users:
- Select specific refrigeration cases/walk-ins
- Assign custom templates and racks
- Manually control system configurations  

→ **Great for detailed design and custom modeling**

---

## 🧰 Template Selection: System Type and Era

System **template** determines performance assumptions, curve data, and equipment configuration.

- **`old`** : Systems designed **before 2010**  
  ↳ Legacy setups with lower efficiency  
- **`new`** : Systems installed **2010–2020**  
  ↳ Moderately efficient with improved practices  
- **`advanced`** : Systems **after 2020**  
  ↳ High-efficiency with modern technologies  

→ Your selection impacts compressor sizing, condenser performance, and load distribution.

---

## ❄️ Temperature Levels: MT and LT Systems

Systems are categorized by suction temperature level:

- **`MT` (Medium Temperature)**  
  Suction Temp ≈ **-6.7 °C (20 °F)** ・ Condenser Temp ≈ **48.9 °C (120 °F)**  
  ↳ Used for dairy, produce, deli, and beverages

- **`LT` (Low Temperature)**  
  Suction Temp ≈ **-31.7 °C (-25 °F)** ・ Condenser Temp ≈ **40.6 °C (105 °F)**  
  ↳ Used for frozen foods and long-term storage  

→ These values drive compressor curve selection and system sizing.

---



## 📜 License

**This is a work in progress**  
Will be distributed under the terms of the **BSD-3-Clause** license.
