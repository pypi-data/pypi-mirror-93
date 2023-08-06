DATA = set()  # type: ignore

IMXX = {
    'SMAP',
    'BMAP',
    'BOMP',
    *[f'ZP{i:02X}' for i in range(1, 5)],
}

RAWD = '____'  # Collect rest of chunk as raw data

SCHEMA = {
    RAWD: DATA,
    'LECF': {
        'LOFF',
        'LFLF'
    },
    'LOFF': DATA,
    'LFLF': {
        'RMIM',
        'RMDA',
        'ROOM',
        'RMSC',
        'SCRP',
        'SOUN',
        'AKOS',
        'COST',
        'CHAR',
        'DIGI',
        'MULT',
        'AWIZ',
        'TALK',
        RAWD
    },
    'ROOM': {
        'RMHD',
        'CYCL',
        'PALS',
        'IMAG',
        'OBIM',
        'BOXD',
        'BOXM',
        'SCAL',
        'RMSC',
        'TRNS',
        'EPAL',
        'CLUT',
        'RMIM',
        'OBCD',
        'EXCD',
        'ENCD',
        'NLSC',
        'LSCR'
    },
    'RMDA': {
        'RMHD',
        'CYCL',
        'TRNS',
        'PALS',
        'OBIM',
        'OBCD',
        'EXCD',
        'ENCD',
        'NLSC',
        'LSC2',
        'LSCR',
        'POLD'
    },
    'RMHD': DATA,
    'RMIM': {
        'RMIH',
        'IM00'
    },
    'TRNS': DATA,
    'EPAL': DATA,
    'CYCL': DATA,
    'PALS': {
        'WRAP'
    },
    'OFFS': DATA,
    'APAL': DATA,
    'WRAP': {
        'OFFS',
        'APAL',
        'SMAP',
        'BOMP',
        'AWIZ',
        'SEQI'
    },
    'IMAG': {
        'WRAP'
    },
    'OBIM': {
        'IMHD',
        'IMAG',
        *[f'IM{i:02X}' for i in range(1, 17)],
    },
    'RMSC': {
        'ENCD',
        'EXCD',
        'OBCD',
        'LSCR'
    },
    'OBCD': {
        'CDHD',
        'OBNA',
        'VERB'
    },
    **{f'IM{i:02X}': IMXX for i in range(17)},
    **{f'ZP{i:02X}': DATA for i in range(1, 5)},
    'BOXD': DATA,
    'BOXM': DATA,
    'CLUT': DATA,
    'SCAL': DATA,
    'RMIH': DATA,
    'AKOS': {
        'AKHD',
        'AKPL',
        'RGBS',
        'AKSQ',
        'AKCH',
        'AKOF',
        'AKCI',
        'AKCD',
        'AKLC',
        'AKST',
        'AKCT',
        'SP2C',
        'SPLF',
        'CLRS',
        'IMGL',
        'SQDB',
        'AKFO'
    },
    'SMAP': DATA,  # ?
    'IMHD': DATA,
    'CDHD': DATA,
    'VERB': DATA,
    'OBNA': DATA,
    'EXCD': DATA,
    'ENCD': DATA,
    'NLSC': DATA,
    'LSCR': DATA,
    'CHAR': DATA,
    'SCRP': DATA,
    'COST': DATA,
    'SOUN': DATA,
    'BOMP': DATA,
    'RNAM': DATA,
    'MAXS': DATA,
    'DROO': DATA,
    'DSCR': DATA,
    'DSOU': DATA,
    'DCOS': DATA,
    'DCHR': DATA,
    'DOBJ': DATA,
    'BMAP': DATA,
    'LSC2': DATA,
    'DIGI': {
        'HSHD',
        'SDAT',
        'SBNG'
    },
    'HSHD': DATA,
    'SDAT': DATA,
    'AKHD': DATA,
    'AKPL': DATA,
    'RGBS': DATA,
    'AKSQ': DATA,
    'AKCH': DATA,
    'AKOF': DATA,
    'AKCI': DATA,
    'AKCD': DATA,
    'AKLC': DATA,
    'AKST': DATA,
    'AKCT': DATA,
    'AKFO': DATA,
    'MULT': {
        'DEFA',
        'WRAP'
    },
    'DEFA': {
        'RGBS',
        'CNVS'
    },
    'AWIZ': {
        'WIZH',
        'WIZD',
        'CNVS',
        'SPOT',
        'RELO',
        'RGBS'
    },
    'WIZH': DATA,
    'WIZD': DATA,
    'CNVS': DATA,
    'SPOT': DATA,
    'RELO': DATA,
    'POLD': DATA,
    'SP2C': DATA,
    'SPLF': DATA,
    'CLRS': DATA,
    'IMGL': DATA,
    'SQDB': {
        'WRAP'
    },
    'SEQI': {
        'NAME',
        'STOF',
        'SQLC',
        'SIZE'
    },
    'NAME': DATA,
    'STOF': DATA,
    'SQLC': DATA,
    'SIZE': DATA,
    'SBNG': DATA,
    'TALK': {
        'HSHD',
        'SDAT',
        'SBNG'
    },

    # HE0
    'DIRI': DATA,
    'DIRR': DATA,
    'DIRS': DATA,
    'DIRN': DATA,
    'DIRC': DATA,
    'DIRF': DATA,
    'DIRM': DATA,
    'DIRT': DATA,
    'DLFL': DATA,
    'DISK': DATA,
    'SVER': DATA,
    'AARY': DATA,
    'INIB': {
        'NOTE'
    },
    'NOTE': DATA,

    # HE2
    'TLKB': {
        'SBNG',
        'TALK'
    },

    # HE4
    'SONG': {
        'SGHD',
        'SGEN',
        'DIGI'
    },
    'SGHD': DATA,
    'SGEN': DATA,

    # LA0
    'ANAM': DATA,
}
