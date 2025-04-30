from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg before importing pyplot
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
import base64

app = Flask(__name__)
crime_data = pd.read_csv("main.csv")
crime_data.fillna(0, inplace=True)

violent_types = ['MURDER', 'ATTEMPT TO MURDER', 'RAPE', 'RIOTS', 'HURT/GREVIOUS HURT']
women_related = ['RAPE', 'DOWRY DEATHS', 'CRUELTY BY HUSBAND OR HIS RELATIVES', 
                'ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY', 'INSULT TO MODESTY OF WOMEN']
property_related = ['THEFT', 'AUTO THEFT', 'BURGLARY', 'ROBBERY', 'DACOITY']
focused_crimes = ['MURDER', 'ATTEMPT TO MURDER', 'RAPE', 'ROBBERY', 'BURGLARY', 
                 'THEFT', 'RIOTS', 'DOWRY DEATHS', 'AUTO THEFT']
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predefined')
def predefined():
    return render_template('predefined.html')

@app.route('/custom')
def custom():
    columns = list(crime_data.columns)
    return render_template('custom.html', columns=columns)
@app.route('/plot', methods=['POST'])
def plot():
    option = request.json.get('option')
    
    try:
        plt.style.use('dark_background')  # Use dark theme for all plots
        fig = plt.figure(figsize=(12, 7), facecolor='#111111')
        
        if option == '1':
            crime_data['Total_Reported'] = crime_data.iloc[:, 3:].sum(axis=1)
            top_states = crime_data.groupby('STATE/UT')['Total_Reported'].sum().nlargest(10)
            
            ax = sns.barplot(x=top_states.values, y=top_states.index, palette='Reds_r', edgecolor='#ff2a6d', linewidth=1)
            plt.title("Top 10 States with Highest IPC Crimes", pad=20, color='white', fontsize=14)
            
            # Add value labels
            for i, v in enumerate(top_states.values):
                ax.text(v + 100, i, f"{v:,}", color='white', va='center')
            
            plt.xlabel("Total Reported Crimes", color='white')
            plt.ylabel("State/UT", color='white')
            plt.xticks(color='white')
            plt.yticks(color='white')

        elif option == '2':
            total_violent = crime_data[violent_types].sum()
            
            # Create explosion effect for emphasis
            explode = [0.05] * len(total_violent)
            
            # Use more distinct colors
            colors = ['#ff0000', '#ff5252', '#ff7b7b', '#ff9e9e', '#ffc9c9']
            
            plt.pie(total_violent, labels=total_violent.index, autopct='%1.1f%%',
                   explode=explode, colors=colors, shadow=True,
                   textprops={'color': 'white', 'fontsize': 10})
            
            plt.title("Violent Crime Distribution", pad=20, color='white', fontsize=14)
            
            # Add white circle in center to make it donut-like
            centre_circle = plt.Circle((0,0), 0.70, fc='#111111')
            fig.gca().add_artist(centre_circle)

        elif option == '3':
            total_women = crime_data[women_related].sum()
            explode = [0.05] * len(total_women)
            colors = ['#ff2a6d', '#ff5c8a', '#ff8fab', '#ffb7c5', '#ffd6e0']
            
            wedges, texts, autotexts = plt.pie(total_women, labels=total_women.index, 
                                              autopct='%1.1f%%', explode=explode, 
                                              colors=colors, shadow=True,
                                              textprops={'color': 'white', 'fontsize': 10})
            
            plt.title("Women-Related Crime Distribution", pad=20, color='white', fontsize=14)
            
            # Make labels more readable
            for text in texts:
                text.set_color('white')
                text.set_fontsize(10)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(10)

        elif option == '4':
            total_property = crime_data[property_related].sum()
            explode = [0.05] * len(total_property)
            colors = ['#ff9500', '#ffaa33', '#ffbf66', '#ffd499', '#ffeacc']
            
            plt.pie(total_property, labels=total_property.index, autopct='%1.1f%%',
                   explode=explode, colors=colors, shadow=True,
                   textprops={'color': 'white', 'fontsize': 10})
            
            plt.title("Property Crime Distribution", pad=20, color='white', fontsize=14)

        elif option == '5':
            focused_data = crime_data.groupby('YEAR')[focused_crimes].sum()
            
            # Use distinct colors for each crime type
            colors = ['#ff0000', '#ff2a6d', '#ff5500', '#ff9500', 
                     '#00a2ff', '#00ffa2', '#a200ff', '#ff00a2', '#00ff55']
            
            ax = focused_data.plot(marker='o', markersize=8, linewidth=2.5, color=colors)
            
            plt.title("Focused Crimes Trend (2014–2020)", pad=20, color='white', fontsize=14)
            plt.xlabel("Year", color='white')
            plt.ylabel("Count", color='white')
            
            # Customize legend
            legend = ax.legend(facecolor='#222', edgecolor='#ff2a6d', 
                              fontsize=9, labelcolor='white')
            
            # Customize grid
            ax.grid(True, color='#333', linestyle='--', alpha=0.5)
            
            # Customize ticks
            ax.tick_params(colors='white')
            
            # Add data labels for last year
            for i, col in enumerate(focused_data.columns):
                last_val = focused_data[col].iloc[-1]
                ax.text(focused_data.index[-1], last_val, f"{last_val:,}", 
                       color=colors[i], ha='left', va='center')

        elif option == '6':
            # Create correlation heatmap with better styling
            plt.figure(figsize=(12, 8))
            sns.heatmap(crime_data[focused_crimes].corr(), annot=True, 
                       cmap='coolwarm', center=0, vmin=-1, vmax=1,
                       annot_kws={'color': 'white', 'fontsize': 9},
                       cbar_kws={'label': 'Correlation Coefficient'})
            
            plt.title("Crime Type Correlation Heatmap", pad=20, color='white', fontsize=14)
            plt.xticks(color='white', rotation=45, ha='right')
            plt.yticks(color='white')

        else:
            return jsonify({'error': 'Invalid option'})

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100, facecolor=fig.get_facecolor())
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close(fig)
        
        return jsonify({'img': f'data:image/png;base64,{plot_url}'})
        
    except Exception as e:
        return jsonify({'error': str(e)})
@app.route('/custom_plot', methods=['POST'])
@app.route('/custom_plot', methods=['POST'])
def custom_plot():
    x = request.form.get("x_col")
    y = request.form.get("y_col")
    plot_type = request.form.get("plot_type")

    try:
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(12, 7), facecolor='#111111')
        
        if plot_type == "bar":
            ax = sns.barplot(data=crime_data, x=x, y=y, palette='Reds_r', 
                            edgecolor='#ff2a6d', linewidth=1)
            
            # Add value labels
            for p in ax.patches:
                ax.annotate(f"{p.get_height():.0f}", 
                           (p.get_x() + p.get_width() / 2., p.get_height()),
                           ha='center', va='center', xytext=(0, 5),
                           textcoords='offset points', color='white')

        elif plot_type == "line":
            ax = plt.plot(crime_data[x], crime_data[y], color='#ff2a6d', 
                         linewidth=2.5, marker='o', markersize=6)[0]
            
            # Add data points labels
            for i, txt in enumerate(crime_data[y]):
                plt.annotate(f"{txt:.0f}", (crime_data[x].iloc[i], txt),
                            textcoords="offset points", xytext=(0,5),
                            ha='center', color='white')

        elif plot_type == "scatter":
            ax = sns.scatterplot(data=crime_data, x=x, y=y, color='#ff2a6d', 
                                s=100, edgecolor='white', linewidth=0.5)
            
            # Add regression line
            sns.regplot(data=crime_data, x=x, y=y, scatter=False, 
                        color='#00a2ff', line_kws={'linestyle':'--'})

        elif plot_type == "pie":
            top_vals = crime_data[x].value_counts().head(10)
            colors = plt.cm.Reds_r(np.linspace(0.2, 0.8, len(top_vals)))
            
            wedges, texts, autotexts = plt.pie(top_vals, labels=top_vals.index, 
                                             autopct='%1.1f%%', colors=colors,
                                             startangle=90, counterclock=False,
                                             wedgeprops={'edgecolor': '#111', 'linewidth': 1},
                                             textprops={'color': 'white', 'fontsize': 9})
            
            # Make labels more readable
            for text in texts:
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_color('white')

        else:
            return jsonify({'error': 'Invalid plot type'})

        plt.title(f"{plot_type.title()} of {x} vs {y}", pad=20, color='white', fontsize=14)
        
        # Style axes
        ax = plt.gca()
        ax.tick_params(colors='white')
        if plot_type != "pie":
            plt.xlabel(x, color='white')
            if y:
                plt.ylabel(y, color='white')
        
        # Add grid for non-pie charts
        if plot_type != "pie":
            ax.grid(True, color='#333', linestyle='--', alpha=0.5)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100, facecolor=fig.get_facecolor())
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close(fig)
        return jsonify({'img': f'data:image/png;base64,{plot_url}'})

    except Exception as e:
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    app.run(debug=True)