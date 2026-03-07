from database import init_db, add_trade

init_db()

sample_trades = [
    (
        "2026-02-01",
        "2026-02-03",
        "GBPJPY",
        "Short",
        "BoE dovish vs BoJ neutral",
        "Macro Divergence",
        2.1,
        "Buen timing tras dato",
        "Esperé confirmación y la entrada fue limpia. Repetir este tipo de paciencia."
    ),
    (
        "2026-02-04",
        "2026-02-05",
        "AUDCAD",
        "Long",
        "RBA hawkish",
        "Central Bank",
        1.2,
        "Setup limpio",
        "La idea estaba bien construida, pero el objetivo pudo haberse estirado algo más."
    ),
    (
        "2026-02-06",
        "2026-02-06",
        "USDJPY",
        "Long",
        "Risk-on",
        "Event",
        -0.8,
        "Entró demasiado pronto",
        "Error de timing. La idea no era mala, pero me precipité antes de confirmación."
    ),
    (
        "2026-02-10",
        "2026-02-12",
        "EURUSD",
        "Short",
        "Fed hawkish vs ECB",
        "Macro Divergence",
        2.5,
        "Muy buena narrativa",
        "La narrativa estaba clara y la ejecución acompañó. Trade muy alineado con el plan."
    )
]

for trade in sample_trades:
    add_trade(*trade)

print("Datos de ejemplo insertados.")