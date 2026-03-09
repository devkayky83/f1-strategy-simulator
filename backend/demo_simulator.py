# DEMO - F1 Strategy Simulator
# Este script demonstra o motor de simulação funcionando
# Funciona para testes rápidos (Não precisa de banco de dados)

import sys
from pathlib import Path

# Adicionar path do projeto
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.simulation_engine import RaceSimulationEngine, compare_strategies
from app.models.circuit import Circuit
from app.models.tire_compound import TireCompound
from app.models.strategy import Strategy


def create_demo_circuit():
    circuit = Circuit(
        id=1,
        name="Monza",
        country="Italy",
        city="Monza",
        lap_distance=5.793,
        total_laps=53,
        total_distance=306.720,
        base_lap_time=81.0,
        track_record=80.411,
        tire_wear_factor=0.9,
        fuel_effect=0.033,
        pit_loss_time=19.0,
        number_of_turns=11,
        drs_zones=2,
        typical_temp=25.0
    )
    
    return circuit



def create_demo_compounds():
    compounds = {
        "C1": TireCompound(
            id=1, name="C1", display_name="Hard",
            base_grip=0.92, degradation_rate=0.015, optimal_life=40,
            optimal_temp_min=90.0, optimal_temp_max=110.0,
            cliff_lap=35, cliff_factor=1.8, warm_up_laps=2, warm_up_penalty=0.4
        ),
        "C2": TireCompound(
            id=2, name="C2", display_name="Medium-Hard",
            base_grip=0.95, degradation_rate=0.022, optimal_life=35,
            optimal_temp_min=85.0, optimal_temp_max=105.0,
            cliff_lap=30, cliff_factor=1.7, warm_up_laps=2, warm_up_penalty=0.35
        ),
        "C3": TireCompound(
            id=3, name="C3", display_name="Medium",
            base_grip=1.00, degradation_rate=0.030, optimal_life=30,
            optimal_temp_min=80.0, optimal_temp_max=100.0,
            cliff_lap=25, cliff_factor=1.6, warm_up_laps=1, warm_up_penalty=0.3
        ),
        "C4": TireCompound(
            id=4, name="C4", display_name="Soft",
            base_grip=1.05, degradation_rate=0.040, optimal_life=25,
            optimal_temp_min=75.0, optimal_temp_max=95.0,
            cliff_lap=20, cliff_factor=1.5, warm_up_laps=1, warm_up_penalty=0.2
        ),
        "C5": TireCompound(
            id=5, name="C5", display_name="Super Soft",
            base_grip=1.10, degradation_rate=0.055, optimal_life=20,
            optimal_temp_min=70.0, optimal_temp_max=90.0,
            cliff_lap=15, cliff_factor=1.4, warm_up_laps=1, warm_up_penalty=0.15
        )
    }
    
    return compounds



def create_strategy_1_stop():
    # Estratégia de 1 parada: Medium -> Hard
    
    strategy = Strategy(
        id=1,
        name="One-Stop: Medium -> Hard\n",
        circuit_id=1,
        total_pit_stops=1,
        strategy_data={
            "pit_stops": [
                {"lap": 1, "compound": "C3", "duration": 2.3},
                {"lap": 28, "compound": "C1", "duration": 2.5}
            ]
        }
    )
    
    return strategy



def create_strategy_2_stop():
    # Estrátegia de 2 paradas: Soft -> Medium -> Hard
    
    strategy = Strategy(
        id=2,
        name="Two-stops: Soft -> Medium -> Hard\n",
        circuit_id=1,
        total_pit_stops=2,
        strategy_data = {
            "pit_stops": [
                {"lap": 1, "compound": "C4", "duration": 2.2},
                {"lap": 18, "compound": "C3", "duration": 2.4},
                {"lap": 37, "compound": "C1", "duration": 2.6}
            ]
        }
    )
    
    return strategy



def create_strategy_aggressive():
    # Estratégia mais agressiva: Soft -> Soft -> Medium
    
    strategy = Strategy(
        id=3,
        name="Agressive: Soft -> Soft -> Medium\n",
        circuit_id=1,
        total_pit_stops=2,
        strategy_data = {
            "pit_stops": [
                {"lap": 1, "compound": "C4", "duration": 2.1},
                {"lap": 20, "compound": "C4", "duration": 2.3},
                {"lap": 40, "compound": "C3", "duration": 2.4}
            ]
        }
    )
    
    return strategy



def demo_single_simulation():
    # Demonstração da simulação
    
    print("\n" + "="*80)
    print("DEMO 1: SIMULAÇÃO DE ESTRATÉGIA ÚNICA")
    print("="*80)
    
    circuit = create_demo_circuit()
    compounds = create_demo_compounds()
    strategy = create_strategy_1_stop()
    
    # Criação do motor de simulação
    engine = RaceSimulationEngine(
        circuit=circuit,
        strategy=strategy,
        tire_compounds=compounds,
        track_temperature=25.0,
        random_seed=42
    )
    
    results = engine.simulate_race()
    
    print("\n Primeiras 10 voltas: \n")
    for lap_data in results["lap_by_lap"][:10]:
        pit_marker = " - PIT" if lap_data["is_pit"] else ""
        print(f" Lap {lap_data['lap']:2d}: {lap_data['time']:6.3f}s [{lap_data['compound']}] Age:{lap_data['tire_age']:2d}{pit_marker}")
        
    return results



def demo_strategy_comparison():
    print("\n" + "="*80)
    print("DEMO 2: COMPARAÇÃO DE ESTRATÉGIAS")
    print("="*80)
    
    circuit = create_demo_circuit()
    compounds = create_demo_compounds()
    
    strategies = [
        create_strategy_1_stop(),
        create_strategy_2_stop(),
        create_strategy_aggressive()
    ]
    
    comparison = compare_strategies(circuit, strategies, compounds)
    
    print(f"\n VENCEDOR: {comparison['best_strategy']}")
    print(f"- Diferença para última: {comparison['time_difference']:.3f}s")
    
    print("\n RANKING: ")
    for i, result in enumerate(comparison['results'], 1):
        fastest_marker = "W" if result.get("is_fastest") else ""
        print(f"\n{i}. {result['strategy_name']}{fastest_marker}")
        print(f"  - Tempo Total: {result['total_race_time_formatted']}")
        print(f"  - Média/Volta: {result['average_lap_time']:.3f}s")
        print(f"  - Volta +Rápida: {result['fastest_lap']:.3f}s")
        print(f"  - Pit Stops: {result['total_pit_stops']} ({result['total_pit_time']:.1f}s)")
        
        
        
def demo_tire_degradation_analysis():
    print("\n" + "="*80)
    print("DEMO 3: ANÁLISE DE DEGRADAÇÃO DE PNEUS")
    print("="*80)
    
    circuit = create_demo_circuit()
    compounds = create_demo_compounds()
    strategy = create_strategy_1_stop()
    
    engine = RaceSimulationEngine(circuit, strategy, compounds, random_seed=42)
    results = engine.simulate_race()
    
    print("\n Análise de Degradação por Stint:")
    
    current_compound = None
    stint_laps = []
    
    for lap_data in results["lap_by_lap"]:
        if current_compound != lap_data["compound"]:
            if stint_laps:
                # Exibe o stint anterior
                average_time = sum(stint_laps) / len(stint_laps)
                degradation = stint_laps[-1] - stint_laps[0]
                print(f"\n [{current_compound}] - {len(stint_laps)} voltas")
                print(f"   - Primeira volta: {stint_laps[0]:.3f}s")
                print(f"   - Última volta: {stint_laps[-1]:.3f}s")
                print(f"   - Média: {average_time:.3f}s")
                print(f"   - Degradação total +{degradation:.3f}s")
                
            stint_laps = []
            current_compound = lap_data["compound"]
            
        if not lap_data["is_pit"]:
            stint_laps.append(lap_data["time"])
            
    
    # Último stint
    if stint_laps:
        average_time = sum(stint_laps) / len(stint_laps)
        degradation = stint_laps[-1] - stint_laps[0]
        print(f"\n [{current_compound}] - {len(stint_laps)} voltas")
        print(f"   - Primeira volta: {stint_laps[0]:.3f}s")
        print(f"   - Última volta: {stint_laps[-1]:.3f}s")
        print(f"   - Média: {average_time:.3f}s")
        print(f"   - Degradação total: {degradation:.3f}s")
        


def main():
    print("\n" + "="*80)
    print("F1 RACE STRATEGY SIMULATOR - DEMONSTRAÇÃO")
    print("="*80)
    
    try:
        demo_single_simulation()
        
        input("\n 1. Pressione ENTER para continuar para a Demo 2...")
        
        demo_strategy_comparison()
        
        input("\n 2. Pressione ENTER para continuar para a Demo 3...")
        
        demo_tire_degradation_analysis()
        
        print("\n" + "="*80)
        print("DEMONSTRAÇÃO COMPLETA!")
        print("="*80)
        print("\n Próximos passos:")
        print("  1. Configure o banco de dados (docker-compose up -d)")
        print("  2. Execute o seed: python database/seeds/initial_data.py")
        print("  3. Inicie a API: uvicorn app.main:app --reload")
        print("  4. Acesse: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n - Erro durante demonstração: {e}")
        import traceback
        traceback.print_exc()
        
        
if __name__ == "__main__":
    main()