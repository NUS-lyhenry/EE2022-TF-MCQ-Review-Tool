#!/usr/bin/env python3
"""
EE2022 Concept Quiz
Interactive conceptual quiz for Electrical Energy Systems.
- Mixes True/False and MCQ questions
- Focuses on lecture-style concepts, not long calculations
- Run: python ee2022_concept_quiz.py
"""

import random
import textwrap
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Question:
    kind: str  # 'tf' or 'mcq'
    topic: str
    prompt: str
    answer: str
    explanation: str
    choices: Optional[List[str]] = None

QUESTIONS: List[Question] = [
    # AC fundamentals / AC power
    Question('tf','AC fundamentals','The RMS value equals peak value divided by sqrt(2) for any AC waveform.','F','This relation is specifically true for sinusoidal waveforms, not arbitrary AC waveforms.'),
    Question('tf','AC fundamentals','For a pure resistor, instantaneous power is always non-negative.','T','p=v*i=v^2/R=i^2R, so it cannot be negative.'),
    Question('tf','AC fundamentals','For ideal inductors and capacitors, average real power over a cycle is zero.','T','They store and return energy, so average real power is zero.'),
    Question('tf','AC fundamentals','In an RL load, current leads voltage.','F','In an inductive load, current lags voltage.'),
    Question('tf','AC fundamentals','In an RC load, current leads voltage.','T','A capacitive load has leading current.'),
    Question('tf','AC fundamentals','The impedance of an inductor increases with frequency.','T','X_L = omega L.'),
    Question('tf','AC fundamentals','The impedance magnitude of a capacitor increases with frequency.','F','X_C = 1/(omega C), so it decreases as frequency increases.'),
    Question('tf','AC fundamentals','At series resonance, a series RLC circuit behaves purely resistively.','T','Inductive and capacitive reactances cancel.'),
    Question('tf','AC fundamentals','Above resonance, a series RLC circuit behaves capacitively.','F','Above resonance, X_L > X_C, so it behaves inductively.'),
    Question('tf','AC power','By convention, an inductive load has positive reactive power.','T','Inductive loads consume positive Q; capacitive loads have negative Q.'),
    Question('tf','AC power','A capacitive load has positive reactive power consumption.','F','Capacitive reactive power is conventionally negative.'),
    Question('mcq','AC power','Which quantity is measured in VAR?', 'C','Reactive power is measured in volt-ampere reactive.', ['Real power','Apparent power','Reactive power','Power factor']),
    Question('mcq','AC power','Complex power is normally calculated as:', 'B','The standard formula is S = V I* using RMS phasors.', ['S = VI','S = V I*','S = V*/I','S = I/V']),
    Question('mcq','AC power','A poor power factor mainly causes:', 'D','Lower PF means higher current for same real power, causing losses and voltage regulation issues.', ['Lower current','Lower apparent power','Zero reactive power','Higher current and losses']),
    Question('tf','AC power','Power factor correction for inductive loads is usually done with a parallel capacitor.','T','A capacitor supplies negative Q to offset inductive positive Q.'),
    Question('tf','AC power','A series capacitor always gives the same result as a parallel capacitor for power factor correction.','F','Series capacitor changes the load voltage/current; parallel capacitor compensates Q seen by source.'),

    # Three phase
    Question('tf','Three-phase','In a balanced three-phase system, phase voltages are separated by 120 degrees.','T','Balanced three-phase sources have equal magnitudes and 120 degree phase displacement.'),
    Question('tf','Three-phase','The neutral current in a balanced three-phase wye load is zero.','T','The three balanced phase currents sum to zero.'),
    Question('tf','Three-phase','In a wye-connected load, line current equals phase current.','T','For Y connection, I_L = I_phase.'),
    Question('tf','Three-phase','In a wye-connected load, line voltage equals phase voltage.','F','For Y connection, V_L = sqrt(3) V_phase.'),
    Question('tf','Three-phase','In a delta-connected load, line voltage equals phase voltage.','T','For delta connection, V_L = V_phase.'),
    Question('tf','Three-phase','In a delta-connected load, line current equals phase current.','F','For delta connection, I_L = sqrt(3) I_phase.'),
    Question('mcq','Three-phase','For a balanced three-phase load, total complex power can be written as:', 'A','For balanced systems, S_3phi = 3 V_phase I_phase*.', ['3 V_phase I_phase*','V_line I_line*','3 V_line I_line*','sqrt(3) V_phase I_phase']),
    Question('mcq','Three-phase','The apparent power of a balanced three-phase system is:', 'C','|S| = sqrt(3) V_line I_line.', ['3 V_line I_line','V_line I_line','sqrt(3) V_line I_line','V_phase I_line']),
    Question('tf','Three-phase','If two balanced three-phase loads draw the same complex power from the same line voltage, their line-current magnitudes are the same.','T','|S| = sqrt(3) V_L I_L, so same |S| and V_L gives same I_L.'),
    Question('tf','Three-phase','Swapping any two phases reverses phase sequence.','T','Interchanging two lines changes ABC to ACB or vice versa.'),

    # Generators
    Question('tf','Synchronous generator','A synchronous generator needs mechanical power input and rotor magnetic field.','T','Mechanical input plus field excitation are required.'),
    Question('tf','Synchronous generator','Increasing turbine input torque mainly controls reactive power output.','F','Mechanical torque mainly controls real power; field excitation controls reactive power.'),
    Question('tf','Synchronous generator','Increasing field excitation mainly affects reactive power output.','T','Excitation changes internal voltage magnitude and hence Q exchange.'),
    Question('tf','Synchronous generator','An over-excited generator supplies reactive power to the grid.','T','Over-excited means Q output is positive.'),
    Question('tf','Synchronous generator','An under-excited generator absorbs reactive power from the grid.','T','Under-excited operation corresponds to negative Q output.'),
    Question('tf','Synchronous generator','The synchronous reactance includes both leakage reactance and armature reaction effect.','T','It represents leakage plus armature reaction in the simplified model.'),
    Question('tf','Synchronous generator','The steady-state stability limit occurs at power angle above 180 degrees.','F','The theoretical maximum real power occurs at delta = 90 degrees.'),
    Question('mcq','Synchronous generator','For a grid-connected synchronous generator, real power output is mainly increased by increasing:', 'B','Mechanical power/torque increases the power angle and real power.', ['Field current','Mechanical torque input','Terminal voltage frequency','Armature resistance']),
    Question('mcq','Synchronous generator','For a grid-connected synchronous generator, reactive power is mainly controlled by:', 'A','Field excitation changes internal generated voltage magnitude.', ['Field excitation','Shaft speed only','Number of poles','Armature resistance only']),
    Question('mcq','Synchronous generator','Low-speed hydro generators usually use:', 'B','Low-speed operation needs many poles, typically salient-pole rotors.', ['Cylindrical rotors','Salient-pole rotors','No rotor field','Single-phase rotors']),
    Question('mcq','Synchronous generator','High-speed steam-turbine generators usually use:', 'A','High-speed turbo-generators use cylindrical/round rotors.', ['Cylindrical rotors','Salient-pole rotors','Squirrel-cage rotors','No rotor']),
    Question('tf','Synchronous generator','Hydro generators generally have more poles than steam-turbine driven generators.','T','Hydro turbines are slower, so they need more poles for the same frequency.'),
    Question('tf','Synchronous generator','A synchronous generator connected to a 50 Hz grid can freely change speed during steady-state operation.','F','It must run at synchronous speed set by grid frequency and pole count.'),

    # Transformers
    Question('tf','Transformer','An ideal transformer can transform DC voltage in steady state.','F','Transformers require changing flux; DC steady state cannot be transformed and may overheat the winding.'),
    Question('tf','Transformer','A transformer changes voltage and current but not frequency.','T','Frequency remains the same across a transformer.'),
    Question('tf','Transformer','Copper losses in a transformer are represented by winding resistance.','T','Copper/winding losses are I^2R losses.'),
    Question('tf','Transformer','Hysteresis and eddy-current losses are core losses.','T','Both occur in the magnetic core.'),
    Question('tf','Transformer','Leakage flux in a transformer is represented by series leakage reactance.','T','Leakage flux is modeled by leakage reactance in series.'),
    Question('tf','Transformer','Magnetizing current is represented by a series resistor in the simplified transformer model.','F','Magnetizing current is represented by a shunt inductive branch.'),
    Question('tf','Transformer','In the transformer short-circuit test, the applied voltage is small and current is near rated.','T','SC test uses low voltage sufficient to circulate rated current.'),
    Question('tf','Transformer','The open-circuit test is mainly used to estimate core loss and magnetizing branch.','T','OC test uses rated voltage with small current, so it reveals shunt branch behavior.'),
    Question('mcq','Transformer','A transformer cannot transform:', 'D','A transformer does not change frequency.', ['Voltage','Current','Impedance level','Frequency']),
    Question('mcq','Transformer','Hysteresis loss can be reduced mainly by:', 'B','Lower-loss magnetic materials and proper design reduce hysteresis; laminations mainly reduce eddy current.', ['Increasing current','Using better magnetic core material','Shorting secondary','Increasing leakage flux']),
    Question('mcq','Transformer','Eddy-current loss can be reduced by:', 'C','Laminated cores interrupt circulating eddy currents.', ['Using solid thick iron core','Increasing frequency','Laminating the core','Removing insulation']),

    # Per-unit
    Question('tf','Per unit','In per-unit analysis, the chosen system power base usually stays the same across transformer zones.','T','Voltage bases change by transformer ratios, while common S_base is usually maintained.'),
    Question('tf','Per unit','Per-unit quantities are actual values divided by base values of the same quantity.','T','p.u. = actual/base.'),
    Question('tf','Per unit','Per-unit analysis helps eliminate explicit ideal transformer ratios in network calculations.','T','A key advantage is simplifying multi-voltage-level systems.'),
    Question('tf','Per unit','The voltage base is normally the same in every zone of a transformer network.','F','Voltage bases change across transformer zones according to transformer ratios.'),
    Question('mcq','Per unit','Which base is commonly kept constant across the whole power system in per-unit analysis?', 'A','S_base is normally chosen once for the whole system.', ['Power base','Voltage base','Current base','Impedance base']),

    # Transmission lines
    Question('tf','Transmission lines','Transmission-line resistance represents ohmic loss in the conductor.','T','Series R represents conductor loss.'),
    Question('tf','Transmission lines','Transmission-line inductance is associated with magnetic flux linkage.','T','Current produces magnetic field, causing inductance.'),
    Question('tf','Transmission lines','Transmission-line capacitance is associated with electric field and charge storage.','T','Conductor voltages create electric fields and capacitance.'),
    Question('tf','Transmission lines','Shunt conductance represents leakage current through insulators/corona paths.','T','G models real leakage from line to ground.'),
    Question('tf','Transmission lines','Shunt capacitance represents real leakage through insulators.','F','C gives charging current; G represents real leakage current.'),
    Question('tf','Transmission lines','For short-line models, shunt admittance is usually neglected.','T','Short lines are modeled mainly with series impedance.'),
    Question('tf','Transmission lines','The nominal-pi medium-line model splits shunt admittance equally at both ends.','T','Y/2 is placed at the sending and receiving ends.'),
    Question('tf','Transmission lines','Underground cables are generally more capacitive than overhead lines.','T','Closer conductor/ground spacing and insulation make cables more capacitive.'),
    Question('tf','Transmission lines','Overhead lines are generally cheaper and easier to repair than underground cables.','T','This is a standard comparison in the lecture.'),
    Question('tf','Transmission lines','Voltage regulation measures how well a line or transformer maintains receiving/secondary voltage as load changes.','T','It compares no-load and full-load receiving/secondary voltages.'),
    Question('mcq','Transmission lines','The primary parameter associated with magnetic flux linkage in a line is:', 'C','Magnetic flux linkage corresponds to inductance.', ['Resistance','Capacitance','Inductance','Conductance']),
    Question('mcq','Transmission lines','Leakage current through imperfect insulation is represented by:', 'D','Conductance is the real shunt leakage path.', ['Series resistance','Series inductance','Shunt capacitance','Shunt conductance']),
    Question('mcq','Transmission lines','The medium-line nominal-pi model includes:', 'C','It includes series impedance Z and shunt admittance Y/2 at each end.', ['Only series R','Only shunt C','Series Z and split shunt Y','Only ideal transformer']),
    Question('tf','Transmission lines','Increasing phase spacing tends to increase line inductance.','T','L is related to log(GMD/GMR); larger spacing increases GMD.'),
    Question('tf','Transmission lines','Bundled conductors usually reduce line inductance.','T','Bundling increases effective GMR, reducing L.'),

    # Induction motors
    Question('tf','Induction motor','An induction motor receives electrical supply at the stator.','T','The stator is supplied; rotor current is induced.'),
    Question('tf','Induction motor','The rotor of a three-phase induction motor normally runs exactly at synchronous speed under load.','F','It must run below synchronous speed in motoring operation to induce rotor current.'),
    Question('tf','Induction motor','At locked rotor, slip is 1.','T','Rotor speed is zero, so s=(Ns-0)/Ns=1.'),
    Question('tf','Induction motor','At synchronous speed, induction motor slip is zero.','T','s=(Ns-Nr)/Ns.'),
    Question('tf','Induction motor','Rotor current frequency is proportional to slip.','T','f_r = s f_s.'),
    Question('tf','Induction motor','Induction motor equivalent circuit is similar to a transformer with a rotating secondary.','T','It is often described as a transformer with a rotating secondary.'),
    Question('tf','Induction motor','Increasing air gap usually improves induction motor power factor.','F','Larger air gap requires more magnetizing current and worsens power factor.'),
    Question('tf','Induction motor','At no load, an induction motor power factor is usually low and lagging.','T','No-load current is largely magnetizing current.'),
    Question('tf','Induction motor','In induction generator operation, slip is negative.','T','Rotor is driven above synchronous speed.'),
    Question('mcq','Induction motor','Rotor current frequency in an induction motor is:', 'B','f_r = s f_s.', ['Equal to supply frequency always','Slip times supply frequency','Always zero','Equal to rotor mechanical speed']),
    Question('mcq','Induction motor','The rotating stator field speed is called:', 'C','It is the synchronous speed.', ['Slip speed','Rotor speed','Synchronous speed','Shaft speed']),
    Question('mcq','Induction motor','The rotor magnetic field speed with respect to the stator is normally:', 'A','Rotor field and stator field rotate synchronously in steady operation.', ['Synchronous speed','Rotor mechanical speed','Zero','Twice synchronous speed']),
    Question('mcq','Induction motor','The rotor magnetic field speed with respect to the rotor is:', 'B','It rotates relative to the rotor at slip speed.', ['Synchronous speed','Slip speed','Line speed','Zero always']),
    Question('tf','Induction motor','Swapping any two stator supply lines reverses the direction of a three-phase induction motor.','T','It reverses phase sequence and rotating field direction.'),

    # Renewable / power electronics / loads / cost
    Question('tf','Renewable energy','A rectifier converts AC to DC.','T','AC-DC conversion is rectification.'),
    Question('tf','Renewable energy','An inverter converts DC to AC.','T','DC-AC conversion is inversion.'),
    Question('tf','Renewable energy','A buck converter steps up DC voltage.','F','A buck converter steps down DC voltage.'),
    Question('tf','Renewable energy','A boost converter output voltage increases as duty cycle increases in the ideal model.','T','For ideal boost, Vout = Vin/(1-D).'),
    Question('tf','Renewable energy','Solar PV converts sunlight directly into DC electrical energy.','T','PV cells produce DC from photons.'),
    Question('tf','Renewable energy','A wind turbine extracts energy from moving air and usually drives a generator.','T','Wind energy is mechanical rotation then electrical generation.'),
    Question('tf','Renewable energy','Wind power is proportional to wind speed squared.','F','Available wind power is proportional to v^3.'),
    Question('tf','Renewable energy','Doubling wind speed ideally increases available wind power by eight times.','T','Power is proportional to v^3.'),
    Question('tf','Renewable energy','A solar PV plant converts mechanical energy into electrical energy.','F','PV converts light/solar energy directly to electrical energy.'),
    Question('tf','Cost of electricity','Demand charge increases with peak demand.','T','Demand charge is based on maximum/billing demand.'),
    Question('tf','Cost of electricity','Energy charge is based on total kWh used.','T','Energy cost is consumption multiplied by energy rate.'),
    Question('tf','Cost of electricity','A low power factor can increase required kVA even when real power is unchanged.','T','S=P/pf, so lower PF raises apparent power.'),
    Question('tf','Cost of electricity','Two customers using the same kWh must always have the same electricity bill.','F','Demand charge, TOU rate, and power factor can make bills different.'),
    Question('tf','Cost of electricity','Time-of-use tariffs charge energy differently depending on when it is used.','T','Peak periods are usually more expensive.'),
]


# For MCQ questions, these explanations are shown when the user selects a wrong option.
# They explain why the selected distractor is not the best answer.
MCQ_CHOICE_EXPLANATIONS: Dict[str, Dict[str, str]] = {
    'Which quantity is measured in VAR?': {
        'A': 'Real power is measured in watts (W), not VAR.',
        'B': 'Apparent power is measured in volt-amperes (VA), not VAR.',
        'D': 'Power factor is dimensionless; it has no unit.',
    },
    'Complex power is normally calculated as:': {
        'A': 'Using S = VI misses the current conjugate, so the sign of reactive power can be wrong.',
        'C': 'V*/I is not the complex-power formula; it resembles an impedance-like ratio, not power.',
        'D': 'I/V is an admittance-like ratio, not complex power.',
    },
    'A poor power factor mainly causes:': {
        'A': 'For the same real power, lower power factor means higher current, not lower current.',
        'B': 'For the same real power, lower power factor means higher apparent power S = P/pf.',
        'C': 'Poor power factor is usually caused by significant reactive power, not zero reactive power.',
    },
    'For a balanced three-phase load, total complex power can be written as:': {
        'B': 'V_line and I_line cannot be directly multiplied as complex phasors for total 3-phase power in this form.',
        'C': 'The factor 3 applies to phase quantities, not line-to-line voltage with line current.',
        'D': 'This gives an apparent-power magnitude style relation only if using line quantities; it is not complex power.',
    },
    'The apparent power of a balanced three-phase system is:': {
        'A': 'The factor is sqrt(3), not 3, when using line-to-line voltage and line current.',
        'B': 'This misses the sqrt(3) factor for a balanced three-phase system.',
        'D': 'Using phase voltage with line current is not the standard apparent power formula here.',
    },
    'For a grid-connected synchronous generator, real power output is mainly increased by increasing:': {
        'A': 'Field current mainly changes internal voltage magnitude and reactive power, not real power directly.',
        'C': 'A grid-connected generator frequency is fixed by the grid; it is not the normal control for real power.',
        'D': 'Armature resistance is a machine parameter, not an operator control for real power output.',
    },
    'For a grid-connected synchronous generator, reactive power is mainly controlled by:': {
        'B': 'Shaft speed is fixed by grid frequency and pole number in synchronism.',
        'C': 'Number of poles is a design parameter, not a reactive-power control during operation.',
        'D': 'Armature resistance is not the normal reactive-power control knob.',
    },
    'Low-speed hydro generators usually use:': {
        'A': 'Cylindrical rotors are preferred for high-speed turbo-generators, not low-speed hydro units.',
        'C': 'A synchronous generator needs a rotor magnetic field.',
        'D': 'Large power-system hydro generators are three-phase machines, not single-phase rotors.',
    },
    'High-speed steam-turbine generators usually use:': {
        'B': 'Salient-pole rotors are more typical for low-speed machines such as hydro generators.',
        'C': 'Squirrel-cage rotors are associated with induction machines, not synchronous turbo-generators.',
        'D': 'A synchronous generator requires a rotor field.',
    },
    'A transformer cannot transform:': {
        'A': 'Voltage transformation is the main purpose of a transformer.',
        'B': 'Current changes inversely with voltage in an ideal transformer.',
        'C': 'Impedance can be reflected across a transformer by the square of the turns ratio.',
    },
    'Hysteresis loss can be reduced mainly by:': {
        'A': 'Increasing current does not target hysteresis loss and can increase heating.',
        'C': 'Shorting the secondary is a test condition, not a method to reduce hysteresis loss.',
        'D': 'Increasing leakage flux is not a method to reduce core hysteresis loss.',
    },
    'Eddy-current loss can be reduced by:': {
        'A': 'A solid thick iron core makes circulating eddy currents easier, increasing eddy-current loss.',
        'B': 'Eddy-current and hysteresis losses generally increase with frequency.',
        'D': 'Removing insulation between laminations would allow larger circulating currents.',
    },
    'Which base is commonly kept constant across the whole power system in per-unit analysis?': {
        'B': 'Voltage base changes between zones according to transformer ratios.',
        'C': 'Current base depends on S_base and V_base, so it changes when voltage base changes.',
        'D': 'Impedance base depends on voltage and power bases, so it changes between zones.',
    },
    'The primary parameter associated with magnetic flux linkage in a line is:': {
        'A': 'Resistance represents ohmic conductor loss, not magnetic flux linkage.',
        'B': 'Capacitance is associated with electric fields and charge storage.',
        'D': 'Conductance represents leakage current paths through insulation/air.',
    },
    'Leakage current through imperfect insulation is represented by:': {
        'A': 'Series resistance represents conductor ohmic loss along the line.',
        'B': 'Series inductance represents magnetic-field effects from line current.',
        'C': 'Shunt capacitance represents charging current due to electric fields, not real leakage current.',
    },
    'The medium-line nominal-pi model includes:': {
        'A': 'A medium line cannot be represented by only series resistance; it needs series impedance and shunt admittance.',
        'B': 'Only shunt capacitance misses the series impedance of the line.',
        'D': 'An ideal transformer is not the transmission-line nominal-pi model.',
    },
    'Rotor current frequency in an induction motor is:': {
        'A': 'Rotor frequency equals supply frequency only at locked rotor, when slip is 1.',
        'C': 'Rotor frequency is zero only if slip is zero, which gives no induction torque in normal motoring.',
        'D': 'Rotor mechanical speed is measured in rpm or rad/s; rotor current frequency is electrical Hz.',
    },
    'The rotating stator field speed is called:': {
        'A': 'Slip speed is the difference between synchronous speed and rotor speed.',
        'B': 'Rotor speed is the mechanical speed of the rotor, usually below synchronous speed in motoring.',
        'D': 'Shaft speed is the mechanical rotor speed, not the stator field speed.',
    },
    'The rotor magnetic field speed with respect to the stator is normally:': {
        'B': 'Rotor mechanical speed is lower than synchronous speed in motoring; the rotor field still rotates at synchronous speed relative to the stator.',
        'C': 'The rotor field is not stationary relative to the stator during normal operation.',
        'D': 'There is no normal steady-state condition where the rotor field rotates at twice synchronous speed relative to the stator.',
    },
    'The rotor magnetic field speed with respect to the rotor is:': {
        'A': 'Synchronous speed is the rotor field speed relative to the stator, not relative to the rotor.',
        'C': 'Line speed is not the relevant induction-motor field-speed term.',
        'D': 'It is zero only at zero rotor current frequency; normally it is slip speed relative to the rotor.',
    },
}

TOPICS = sorted(set(q.topic for q in QUESTIONS))


def normalize_answer(ans: str) -> str:
    return ans.strip().upper()


def ask_question(q: Question, num: int, total: int) -> bool:
    print('\n' + '=' * 72)
    print(f'Question {num}/{total}  [{q.topic}]  ({"True/False" if q.kind == "tf" else "MCQ"})')
    print(textwrap.fill(q.prompt, width=72))
    if q.kind == 'mcq':
        letters = 'ABCD'
        for letter, choice in zip(letters, q.choices or []):
            print(f'  {letter}. {choice}')
        valid = set(letters[:len(q.choices or [])])
    else:
        print('  T. True')
        print('  F. False')
        valid = {'T', 'F'}

    while True:
        ans = normalize_answer(input('Your answer: '))
        if ans in {'Q', 'QUIT', 'EXIT'}:
            raise KeyboardInterrupt
        if ans in valid:
            break
        print(f'Please enter one of: {", ".join(sorted(valid))}. Or Q to quit.')

    correct = ans == q.answer
    print('✅ Correct!' if correct else f'❌ Wrong. Correct answer: {q.answer}')

    if not correct and q.kind == 'mcq':
        choice_text = (q.choices or [])[ord(ans) - ord('A')]
        correct_text = (q.choices or [])[ord(q.answer) - ord('A')]
        print('Your choice:', textwrap.fill(f'{ans}. {choice_text}', width=72))
        wrong_reason = MCQ_CHOICE_EXPLANATIONS.get(q.prompt, {}).get(ans)
        if wrong_reason:
            print('Why this option is wrong:', textwrap.fill(wrong_reason, width=72))
        print('Correct option:', textwrap.fill(f'{q.answer}. {correct_text}', width=72))

    print('Explanation:', textwrap.fill(q.explanation, width=72))
    return correct


def choose_topics() -> List[str]:
    print('\nAvailable topics:')
    for i, topic in enumerate(TOPICS, 1):
        count = sum(1 for q in QUESTIONS if q.topic == topic)
        print(f'{i:2d}. {topic} ({count})')
    print(' A. All topics')
    raw = input('\nChoose topic numbers separated by comma, or A for all: ').strip().upper()
    if raw in {'', 'A', 'ALL'}:
        return TOPICS
    selected = []
    for part in raw.split(','):
        part = part.strip()
        if part.isdigit() and 1 <= int(part) <= len(TOPICS):
            selected.append(TOPICS[int(part) - 1])
    return selected or TOPICS


def main() -> None:
    print('EE2022 Concept Quiz')
    print('Type Q at any answer prompt to quit.\n')
    topics = choose_topics()
    pool = [q for q in QUESTIONS if q.topic in topics]

    mode = input('\nQuestion type: [A]ll, [T]rue/False only, [M]CQ only? ').strip().upper()
    if mode == 'T':
        pool = [q for q in pool if q.kind == 'tf']
    elif mode == 'M':
        pool = [q for q in pool if q.kind == 'mcq']

    if not pool:
        print('No questions found for that selection.')
        return

    random.shuffle(pool)
    raw_n = input(f'How many questions? 1-{len(pool)} [default 20]: ').strip()
    try:
        n = int(raw_n) if raw_n else 20
    except ValueError:
        n = 20
    n = max(1, min(n, len(pool)))
    selected = pool[:n]

    score = 0
    wrong = []
    try:
        for i, q in enumerate(selected, 1):
            ok = ask_question(q, i, n)
            if ok:
                score += 1
            else:
                wrong.append(q)
    except KeyboardInterrupt:
        print('\nQuiz stopped early.')

    attempted = score + len(wrong)
    print('\n' + '=' * 72)
    if attempted:
        print(f'Score: {score}/{attempted} = {score/attempted*100:.1f}%')
    else:
        print('No questions attempted.')

    if wrong:
        print('\nReview wrong questions:')
        for q in wrong:
            print(f'- [{q.topic}] {q.prompt}')
            if q.kind == 'mcq' and q.choices:
                correct_text = q.choices[ord(q.answer) - ord('A')]
                print(f'  Correct: {q.answer}. {correct_text}')
            else:
                print(f'  Correct: {q.answer}')
            print(f'  Explanation: {q.explanation}')


if __name__ == '__main__':
    main()
