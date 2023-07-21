pars = {
        # Pool sizes
        "PSIItot": 2.5,  # [mmol/molChl] total concentration of PSII
        "PQtot": 20,  # [mmol/molChl]
        "APtot": 50,  # [mmol/molChl] Bionumbers ~2.55mM (=81mmol/molChl)
        "PsbStot": 1,  # [relative] LHCs that get phosphorylated and protonated
        "Xtot": 1,  # [relative] xanthophylls
        "O2ex": 8,  # external oxygen, kept constant, corresponds to 250 microM, corr. to 20%
        "Pi": 0.01,
        # Rate constants and key parameters
        "kCytb6f": 0.104,  # a rough estimate of the transfer from PQ to cyt that is equal to ~ 10ms
        # [1/s*(mmol/(s*m^2))] - gets multiplied by light to determine rate
        "kActATPase": 0.01,  # paramter relating the rate constant of activation of the ATPase in the light
        "kDeactATPase": 0.002,  # paramter relating the deactivation of the ATPase at night
        "kATPsynthase": 20.0,
        "kATPconsumption": 10.0,
        "kPQred": 250.0,  # [1/(s*(mmol/molChl))]
        "kH": 5e9,  # Heatdisipation (rates)
        "kF": 6.25e8,  # fluorescence 16ns
        "kP": 5e9,  # original 5e9 (charge separation limiting step ~ 200ps) - made this faster for higher Fs fluorescence (express in unites of time
        "kPTOX": 0.01,  # ~ 5 electrons / seconds. This gives a bit more (~20)
        "pHstroma": 7.8,  # [1/s] leakage rate
        "kleak": 1000,
        "bH": 100,  # proton buffer: ratio total / free protons
        "HPR": 14.0 / 3.0,
        # Parameter associated with xanthophyll cycle
        "kDeepoxV": 0.0024,  # Aktivierung des Quenchings
        "kEpoxZ": 0.00024,  # 6.e-4,  #converted to [1/s]   # Deaktivierung
        "KphSatZ": 5.8,  # [-] half-saturation pH value for activity de-epoxidase, highest activity at ~pH 5.8
        "nHX": 5.0,  # [-] hill-coefficient for activity of de-epoxidase
        "Kzsat": 0.12,  # [-], half-saturation constant (relative conc. of Z) for quenching of Z
        # Parameter associated with PsbS protonation
        "nHL": 3,
        "kDeprot": 0.0096,
        "kProt": 0.0096,
        "KphSatLHC": 5.8,
        # Fitted quencher contribution factors
        "gamma0": 0.1,  # slow quenching of Vx present despite lack of protonation
        "gamma1": 0.25,  # fast quenching present due to the protonation
        "gamma2": 0.6,  # slow quenching of Zx present despite lack of protonation
        "gamma3": 0.15,  # fastest possible quenching
        # Physical constants
        "F": 96.485,  # Faraday constant
        "R": 8.3e-3,  # universal gas constant
        "T": 298,  # Temperature in K - for now assumed to be constant at 25 C
        # Standard potentials and DG0ATP
        "E0QAQAm": -0.140,
        "E0PQPQH2": 0.354,
        "E0PCPCm": 0.380,
        "DG0ATP": 30.6,  # 30.6kJ/mol / RT
        # PFD
        "PFD": 100,
    }