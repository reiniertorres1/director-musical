from genres.timba.prompt_builder import build_timba_prompt
from genres.timba.arrangement import TOTAL_BARS


assert TOTAL_BARS == 200, (
    f"ERROR: La estructura deberia tener 200 compases, "
    f"pero tiene {TOTAL_BARS}."
)


test_prompt = build_timba_prompt(
    topic="Una relacion donde una persona ya se canso de las mentiras",
    mood="Energetic, confident and playful",
    extra_instructions=(
        "The song should begin melodically and progressively "
        "become more aggressive and danceable."
    )
)


print("======================================")
print("TIMBA ENGINE TEST")
print("======================================")
print()
print(f"Total de compases: {TOTAL_BARS}")
print()
print("RESULTADO: TODO CORRECTO")
print()
print(test_prompt)
