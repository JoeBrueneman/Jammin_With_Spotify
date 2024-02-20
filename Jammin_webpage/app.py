from flask import Flask, request, render_template
import pickle

# Load the model
model_pkl_file = "song_model.pkl" 
with open(model_pkl_file, 'rb') as file:  
    model = pickle.load(file)


# Create Flask routes
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract input features from the request
    feature1 = float(request.form['feature1'])
    feature2 = float(request.form['feature2'])

    # Preprocess the input features
    # Make predictions using the loaded model
    prediction = model.predict([[feature1, feature2]])

    return render_template('index.html', prediction=prediction[0])

# Run the Flask App locally
if __name__ == '__main__':
    app.run(debug=True)