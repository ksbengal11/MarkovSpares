
from flask import Flask, render_template, request
from wtforms import Form, TextField, validators, SubmitField, SelectField, DecimalField, IntegerField

#import MarkovCalculator

# App config
DEBUG=True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET KEY']= '7d441f27d441f27567d441f2b6176a'

# Make the WSGI interface available at the top level so wfastsgi can find it
wsgi_app = app.wsgi_app

# Entry choices for leadtime and installation time duration
DURATION = [('Year(s)', 'Year(s)'), ('Month(s)', 'Month(s)'),
            ('Week(s)', 'Week(s)'), ('Day(s)', 'Day(s)')]

class MarkovForm(Form):
    """Class for reading form paramters and validating them

    Args:
        duration_leadTime:          Duration of the equipment lead time (i.e. Week(s), Month(s), etc.)
        duration_installationTime:  Duration of the equipment installlation time (i.e. Week(s), Month(s), etc.)
        units:                      Unit count
        failureRate:                Unit failure rate
        leadTime:                   Unit lead time
        installlationTime:          Unit installation time
    """

    duration_leadTime = SelectField(label="Duration", choices=DURATION)
    duration_installationTime = SelectField(label="Duration", choices=DURATION)

    units = IntegerField(label='Units',
                        validators=[validators.required(message='Number of units required'),
                                    validators.number_range(2,
                                        message='Number of units has to be greater than 2')])

    failureRate = DecimalField(label='Failure rate', 
                        validators=[validators.required(message='Failure rate required'),
                                    validators.number_range(0,
                                        message='Failure rate must be greater than 0')])

    leadTime = TextField(label='Lead time',
                        validators=[validators.required(message='Lead time required'),
                                    validators.number_range(0,
                                        message='Lead time must be greater than 0')])

    installationTime = TextField(label='Installation time',
                        validators=[validators.required(message='Installation time required'),
                                    validators.number_range(0,
                                        message='Installation time must be greater than 0')])

def calculateProbabilities(installationTime, failureRate, leadTime,
                            d_leadTime, d_installationTime, unitCount):
    """Function for instantiating Markov calculator and calculating the probability of contingences
       for each spare level.

       Args:
            installationTime:   Unit installation time
            failureRate:        Unit failure rate
            leadTime:           Unit lead time
            d_leadTime:         Duration of the lead time (i.e. weeks, months, etc.)
            d_installationTime: Duration of the installlation time (i.e. weeks, months, etc.)
            unitCount:          Number of units

      Returns:
            groupProbability:   Probability of unit availability at each contingency level for
                                a given number of spares
    """

    # Instantiate the Markov calcuator
    calculator = MarkovCalculator.MarkovCalculator(unitCount, leadTime, installationTime, failureRate,
                                                    d_installationTime, d_leadTime)

    # Compute the transition matrices
    transition_matrices = {'0 spare': calculator.get_0spare_transition_matrix(),
                           '1 spare': calculator.get_1spare_transition_matrix(),
                           '2 spare': calculator.get_2spare_transition_matrix()
                           }

    # Calculate the steady state probability of each transition matrix
    steady_state_matrices = { '0 spare': calculator.calculate_steadyState(transition_matrices['0 spare']),
                              '1 spare': calculator.calculate_steadyState(transition_matrices['1 spare']),
                              '2 spare': calculator.calculate_steadyState(transition_matrices['2 spare'])
                            }

    # Calculat the group probability of steady state matrix for each spare
    group_probability = { '0': calculator.calculate_groupProbability(steady_state_matrices['0 spare'], 0),
                          '1': calculator.calculate_groupProbability(steady_state_matrices['1 spare'], 1),
                          '2': calculator.calculate_groupProbability(steady_state_matrices['2 spare'], 2)
                        }

    return group_probability

@app.route('/about')
def about():
    return render_template('about.html')

# Default route
@app.route('/', methods=['GET','POST'])
def markov():
    form = MarkovForm(request.form)

    #TODO For debugging purposes only - remove
    print form.errors

    if request.method == 'POST':
        # Read form parameters
        units = request.form['units']
        failureRate = request.form['failureRate']
        leadTime=request.form['leadTime']
        installationTime=request.form['installationTime']
        duration_leadTime = request.form['duration_leadTime']
        duration_installationTime = request.form['duration_installationTime']

        # Calculate group probability if validation passes
        if form.validate():
            probability = calculateProbabilities(installationTime, failureRate, leadTime,
                                duration_leadTime, duration_installationTime, units)

            return render_template('markov.html', form=form, result=probability)

    return render_template('markov.html', form=form, result=None)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
