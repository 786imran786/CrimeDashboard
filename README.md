# CrimeDashboard
 Crime Data Analysis &amp; Visualization in Python 🐍  Just wrapped up an insightful project using Pandas, Matplotlib, and Seaborn to dig deep into crime statistics across Indian districts and states 📊🇮🇳
# Crime Statistics Dashboard - India

![Dashboard Screenshot](static/images/dashboard-screenshot.png)

## Overview

This interactive dashboard visualizes crime statistics across India in 2014. Built with Python Flask and modern web technologies, it provides both predefined analyses and customizable visualizations of crime patterns.

## Features

- **Predefined Crime Analysis**: 6 specialized visualizations including:
  - Top crime states
  - Violent crime distribution
  - Women-related crimes
  - Property crimes
  - Crime trends over time
  - Crime type correlations

- **Custom Analysis**: Build your own visualizations by selecting:
  - X/Y axis columns
  - Plot type (bar, line, scatter, pie)

- **Dark Neon Theme**: Cohesive visual design with crime-themed aesthetics

- **Responsive Design**: Works on desktop and mobile devices

## Technologies Used

### Backend
- Python 3
- Flask (Web Framework)
- Pandas (Data Analysis)
- Matplotlib/Seaborn (Visualization)

### Frontend
- HTML5, CSS3
- JavaScript (Interactive elements)
- Plotly.js (Alternative visualizations)

### Data
- National Crime Records Bureau (NCRB) dataset
- Preprocessed CSV format

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/crime-statistics-dashboard.git
   cd crime-statistics-dashboard
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the dashboard at:
   ```
   http://localhost:5000
   ```

## Project Structure

```
crime-dashboard/
├── app.py               # Main Flask application
├── main.csv             # Crime dataset
├── requirements.txt     # Python dependencies
├── static/
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   └── images/          # Static images
└── templates/           # HTML templates
    ├── base.html        # Base template
    ├── index.html       # Home page
    ├── predefined.html  # Predefined analysis
    ├── custom.html      # Custom analysis
    └── about.html       # About page
```

## Usage Guide

1. **Home Page**: Overview of dashboard capabilities
2. **Predefined Analysis**: Select from 6 specialized crime visualizations
3. **Custom Analysis**: Create your own visualizations by choosing:
   - Data columns for X/Y axes
   - Plot type (bar, line, scatter, pie)
4. **About Page**: Developer information and project background

## Customization

To use your own dataset:
1. Replace `main.csv` with your data file
2. Update column names in `app.py` if different
3. Modify visualization parameters as needed

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

**Mohd Imran Siddiqui**  
- GitHub: [@786imran786](https://github.com/786imran786)
- Email: mohdimransid786@gmail.com
- LinkedIn: [yourprofile](https://linkedin.com/in/imransiddiqui786)

---

*This project was developed as part of academic studies at Lovely Professional University, specializing in Data Science.*
