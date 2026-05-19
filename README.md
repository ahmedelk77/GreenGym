
# **Leveraging Neural Networks & Machine Learning for RANS Model Discovery**

## **Project Overview**

This project integrates **Sparse Identification of Non-Linear Systems (SINDy)** and **Physics-Informed Neural Networks (PINN)** to predict **Reynolds Stresses** in **Poiseuille** and **Couette** turbulent flows. The objective is to improve upon the traditional **Reynolds-Averaged Navier-Stokes (RANS)** models, particularly the **SST-kω** model, using a data-driven approach leveraging **DNS** data. The project demonstrates a significant reduction in **Root Mean Square Error (RMSE)** between **DNS** and **RANS** predictions across multiple Reynolds numbers, both in **Channel Flow** and **Couette Flow**.

### Key Objectives:
- Develop data-driven models to predict turbulent Reynolds stresses.
- Discover governing equations using **SINDy** to inform the **PINN**.
- Compare the **PINN** performance with **RANS** and **DNS** results, highlighting the improvements achieved.

---

## **Repository Structure**

\`\`\`bash
Leveraging_NN_ML_for_RANS_Model_Discovery/
│
├── Images/                                      # Contains figures used in the project
├── Neural Networks Codes/                       # Contains the neural network models
│   ├── PINN/                                    # Physics-Informed Neural Network model
│   │   ├── DNS_data/                            # DNS data used for PINN training
│   │   ├── model_files/                         # Model files for the PINN
│   │   ├── Result_Comparison/                   # Comparison between DNS and RANS results
│   │   ├── results/                             # Results of the PINN model predictions
│   │   ├── Save_models/                         # Saved models from training
│   │   ├── Data_Preprocessing.ipynb             # Data preprocessing notebook
│   └── Simple Neural Network/                   # A simple NN approach for RANS model prediction
│       ├── K Optimisation/                      # Files for optimizing the K factor
│       └── Keras Reynold Stress Tensor Predictor # Keras-based NN models
│
├── PySINDy Codes/                               # PySINDy code for discovering governing equations
├── README.txt                                   # ReadMe file
├── Report.pdf                                   # Project report
└── Scientific_Paper.pdf                         # Related scientific paper
\`\`\`

---

## **System Requirements**

- **Operating System**: Windows, macOS, or Linux
- **Hardware**: Minimum 8GB RAM (16GB recommended)

## **Software and Tools**

- **Python 3.8+**
- **Jupyter Notebook**
- Libraries:
  - \`numpy\`
  - \`pandas\`
  - \`matplotlib\`
  - \`seaborn\`
  - \`scipy\`
  - \`scikit-learn\`
  - \`tensorflow\`
  - \`torch\`
  - \`pysindy\`
  - \`sympy\`
  - \`plotly\`

Install the necessary libraries:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

---

## **Data Description**

The project utilizes **DNS data** for **Channel** and **Couette** flows at various **Reynolds numbers** ranging from 182 to 5200 for channels and from 93 to 543 for Couette. The data is crucial in training and validating the models.

### Key Variables:
- **Mean Velocity Fields** (U, W)
- **Streamwise Velocity Gradients** (dU/dy)
- **Reynolds Stresses** (u'u', v'v', w'w', u'v')
- **Turbulent Kinetic Energy** (k)
- **Pressure Fields** (P)

<p align="center">
  <img src="./Images/Figure1.png" alt="Raw and Interpolated DNS and RANS Data" />
</p>

Figure 1 demonstrates the mirroring and interpolation functions applied to preprocess the DNS and RANS data, necessary for model training and improving data diversity.

---

## **Modeling Process**

### **1. Data Preprocessing**

The DNS dataset provides partial flow domain data, which required preprocessing through **mirroring** and **cubic spline interpolation** to complete the domain. This process is critical for enhancing the training dataset's coverage and ensuring consistency with DNS data.

<p align="center">
  <img src="./Images/Figure2.png" alt="Preprocessing Comparison of RANS and DNS Data" />
</p>

### **2. Governing Equation Discovery Using PySINDy**

The **SINDy** approach was applied to discover governing equations for turbulent flow prediction. This process led to simplified and accurate equations for both the **x-momentum** and **y-momentum** components.

#### Example x-momentum equation:

\`\`\`python
momentum_x = -dP/dx - ρ * duv/dy + ν * d²U/dy²
\`\`\`

The identified equations were then embedded into the **PINN** model to enforce physical constraints during training.

### **3. Physics-Informed Neural Network (PINN)**

The **PINN** architecture integrates physics-based constraints into a neural network model. The loss function includes **mean square error**.

<p align="center">
  <img src="./Images/Figure10.png" alt="PINN Model Architecture" />
</p>

The model learns to predict Reynolds stresses, ensuring that the output satisfies both **boundary conditions** and **momentum conservation**.

### **4. Results Comparison**

The results from the **PINN** model were compared against traditional **RANS** and **DNS** data, with significant improvements in prediction accuracy.

<p align="center">
  <img src="./Images/Figure12.png" alt="Comparison of Results" />
</p>

---

## **Key Results**

| Model Type   | RMSE Improvement (%) |
|--------------|----------------------|
| **Channel**  | 81.29%               |
| **Couette**  | 90.3%                |

<p align="center">
  <img src="./Images/Figure13.png" alt="RMSE for Channel Flow" />
</p>

<p align="center">
  <img src="./Images/Figure14.png" alt="RMSE for Couette Flow" />
</p>

---

## **How to Run the Project**

1. Clone the repository:

   \`\`\`bash
   git clone https://github.com/Yass123krk/Portfolio.git
   cd Portfolio/Projects/Leveraging_NN_ML_for_RANS_Model_Discovery
   \`\`\`

2. Install the required Python packages:

   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. Run the Jupyter Notebook for data preprocessing:

   \`\`\`bash
   jupyter notebook Neural_Networks_Codes/PINN/Data_Preprocessing.ipynb
   \`\`\`

4. Train the PINN model:

   \`\`\`bash
   python Neural_Networks_Codes/PINN/train_PINN.py
   \`\`\`

5. View results and compare RANS and DNS:

   \`\`\`bash
   python Neural_Networks_Codes/PINN/compare_results.py
   \`\`\`

---

## **Contact Information**

For any inquiries or suggestions, feel free to contact me at [your-email@example.com].

---

## **References**

1. M. Lee, R.D. Moser, "Direct numerical simulation of turbulent channel flow up to Re 5200", *Journal of Fluid Mechanics*, 774, 2015.
2. S. L. Brunton, J. L. Proctor, J. N. Kutz, "Discovering governing equations from data by sparse identification", *Proceedings of the National Academy of Sciences*, 2016.

