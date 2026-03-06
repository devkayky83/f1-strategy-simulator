# Script para popular banco de dados com dados iniciais
# Circuitos e compostos de pneus reais da F1

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models import Circuit, TireCompound


def create_tire_compounds(db: Session):
    print("Criando compostos de pneus...")
    
    compounds_data = [
        {
            "name": "C1",
            "display_name": "Hard (C1)",
            "base_grip": 0.92,
            "degradation_rate": 0.015,
            "optimal_life": 40,
            "optimal_temp_min": 90.0,
            "optimal_temp_max": 110.0,
            "working_range_min": 80.0,
            "working_range_max": 120.0,
            "color_code": "#FFFFFF",
            "color_name": "White",
            "cliff_lap": 35,
            "cliff_factor": 1.8,
            "warm_up_laps": 2,
            "warm_up_penalty": 0.4,
            "dry_performance": 1.0,
            "wet_performance": 0.0,
            "description": "Composto mais duro, maior durabilidade, demora mais para chegar no ponto ideal de velocidade",
            "typical_usage": "Circuitos com alta abrasividade e longas stints"
        },
        {
            "name": "C2",
            "display_name": "Medium-Hard (C2)",
            "base_grip": 0.95,
            "degradation_rate": 0.022,
            "optimal_life": 35,
            "optimal_temp_min": 85.0,
            "optimal_temp_max": 105.0,
            "working_range_min": 75.0,
            "working_range_max": 115.0,
            "color_code": "#FFFF00",
            "color_name": "Yellow",
            "cliff_lap": 30,
            "cliff_factor": 1.7,
            "warm_up_laps": 2,
            "warm_up_penalty": 0.35,
            "dry_performance": 1.0,
            "wet_performance": 0.0,
            "description": "Composto intermediário-duro",
            "typical_usage": "Boa opção para stints médias"
        },
        {
            "name": "C3",
            "display_name": "Medium (C3)",
            "base_grip": 1.00,
            "degradation_rate": 0.030,
            "optimal_life": 30,
            "optimal_temp_min": 80.0,
            "optimal_temp_max": 100.0,
            "working_range_min": 70.0,
            "working_range_max": 110.0,
            "color_code": "#FFFF00",
            "color_name": "Yellow",
            "cliff_lap": 25,
            "cliff_factor": 1.6,
            "warm_up_laps": 1,
            "warm_up_penalty": 0.3,
            "dry_performance": 1.0,
            "wet_performance": 0.0,
            "description": "Composto médio, equilíbrio entre performance e durabilidade",
            "typical_usage": "Versátil, funciona na maioria dos circuitos"
        },
        {
            "name": "C4",
            "display_name": "Soft (C4)",
            "base_grip": 1.05,
            "degradation_rate": 0.040,
            "optimal_life": 25,
            "optimal_temp_min": 75.0,
            "optimal_temp_max": 95.0,
            "working_range_min": 65.0,
            "working_range_max": 105.0,
            "color_code": "#FF0000",
            "color_name": "Red",
            "cliff_lap": 20,
            "cliff_factor": 1.5,
            "warm_up_laps": 1,
            "warm_up_penalty": 0.2,
            "dry_performance": 1.0,
            "wet_performance": 0.0,
            "description": "Composto macio, alto grip e velocidade imediata, mas degrada rápido",
            "typical_usage": "Qualifying, stints curtas, undercut"
        },
        {
            "name": "C5",
            "display_name": "Soft (C5)",
            "base_grip": 1.10,
            "degradation_rate": 0.055,
            "optimal_life": 20,
            "optimal_temp_min": 70.0,
            "optimal_temp_max": 90.0,
            "working_range_min": 60.0,
            "working_range_max": 100.0,
            "color_code": "#FF0000",
            "color_name": "Red",
            "cliff_lap": 15,
            "cliff_factor": 1.4,
            "warm_up_laps": 1,
            "warm_up_penalty": 0.15,
            "dry_performance": 1.0,
            "wet_performance": 0.0,
            "description": "Composto mais macio, máximo grip mas vida muito mais curta",
            "typical_usage": "Circuitos de baixa abrasividade, qualifying"
        },
        {
            "name": "INTERMEDIATE",
            "display_name": "Intermediate",
            "base_grip": 0.85,
            "degradation_rate": 0.025,
            "optimal_life": 30,
            "optimal_temp_min": 50.0,
            "optimal_temp_max": 70.0,
            "working_range_min": 40.0,
            "working_range_max": 80.0,
            "color_code": "#00FF00",
            "color_name": "Green",
            "cliff_lap": 25,
            "cliff_factor": 1.3,
            "warm_up_laps": 2,
            "warm_up_penalty": 0.5,
            "dry_performance": 0.3,
            "wet_performance": 0.9,
            "description": "Para pista molhada/secando",
            "typical_usage": "Chuva leve ou pista secando"
        },
        {
            "name": "WET",
            "display_name": "Full Wet",
            "base_grip": 0.75,
            "degradation_rate": 0.020,
            "optimal_life": 25,
            "optimal_temp_min": 40.0,
            "optimal_temp_max": 60.0,
            "working_range_min": 30.0,
            "working_range_max": 70.0,
            "color_code": "#0000FF",
            "color_name": "Blue",
            "cliff_lap": 20,
            "cliff_factor": 1.2,
            "warm_up_laps": 3,
            "warm_up_penalty": 0.8,
            "dry_performance": 0.0,
            "wet_performance": 1.0,
            "description": "Para chuva forte",
            "typical_usage": "Chuva pesada, muita água na pista"
        }
    ]
    
    for compound_data in compounds_data:
        compound = TireCompound(**compound_data)
        db.add(compound)
        print(f" ✓ {compound.display_name}")
        
    db.commit()
    print(f" - {len(compounds_data)} compostos criados!\n")
    
    
    
def create_circuits(db: Session):
        print("Criando circuitos...")
        
        circuits_data = [
            {
                "name": "Monaco",
                "country": "Monaco",
                "city": "Monte Carlo",
                "lap_distance": 3.337,
                "total_laps": 78,
                "total_distance": 260.286,
                "base_lap_time": 72.0,
                "track_record": 70.246,
                "record_holder": "Lewis Hamilton",
                "record_year": 2021,
                "tire_wear_factor": 0.7,
                "fuel_effect": 0.025,
                "pit_loss_time": 25.0,
                "number_of_turns": 19,
                "longest_straight": 350,
                "drs_zones": 1,
                "track_type": "street",
                "direction": "clockwise",
                "typical_temp": 22.0,
                "rain_probability": 0.05,
                "first_grand_prix": 1950,
                "description": "O circuito de rua mais icônico da F1, estreito e cheio de curvas, aqui não vence o mais rápido e sim o mais técnico",
                "elevation_change": 42.0,
                "is_active": True
            },
            {
                "name": "Spa-Francorchamps",
                "country": "Belgium",
                "city": "Spa",
                "lap_distance": 7.004,
                "total_laps": 44,
                "total_distance": 308.052,
                "base_lap_time": 105.0,
                "track_record": 103.139,
                "record_holder": "Valtteri Bottas",
                "record_year": 2018,
                "tire_wear_factor": 1.1,
                "fuel_effect": 0.035,
                "pit_loss_time": 20.0,
                "number_of_turns": 19,
                "longest_straight": 750,
                "drs_zones": 2,
                "track_type": "permanent",
                "direction": "clockwise",
                "typical_temp": 18.0,
                "rain_probability": 0.35,
                "first_grand_prix": 1950,
                "description": "Circuito lendário com a característica curva ascendente Eau Rouge, muito rápido",
                "elevation_change": 105.0,
                "is_active": True
            },
            {
                "name": "Monza",
                "country": "Italy",
                "city": "Monza",
                "lap_distance": 5.793,
                "total_laps": 53,
                "total_distance": 306.720,
                "base_lap_time": 81.0,
                "track_record": 80.411,
                "record_holder": "Rubens Barrichello",
                "record_year": 2004,
                "tire_wear_factor": 0.9,
                "fuel_effect": 0.033,
                "pit_loss_time": 19.0,
                "number_of_turns": 11,
                "longest_straight": 1150,
                "drs_zones": 2,
                "track_type": "permanent",
                "direction": "clockwise",
                "typical_temp": 25.0,
                "rain_probability": 0.15,
                "first_grand_prix": 1950,
                "description": "Templo da velocidade, circuito mais rápido do calendário, aqui motor forte fala alto",
                "elevation_change": 23.0,
                "is_active": True
            },
            {
                "name": "Silverstone",
                "country": "United Kingdom",
                "city": "Silverstone",
                "lap_distance": 5.891,
                "total_laps": 52,
                "total_distance": 306.198,
                "base_lap_time": 86.0,
                "track_record": 85.442,
                "record_holder": "Max Verstappen",
                "record_year": 2020,
                "tire_wear_factor": 1.15,
                "fuel_effect": 0.032,
                "pit_loss_time": 20.5,
                "number_of_turns": 18,
                "longest_straight": 730,
                "drs_zones": 2,
                "track_type": "permanent",
                "direction": "clockwise",
                "typical_temp": 20.0,
                "rain_probability": 0.40,
                "first_grand_prix": 1950,
                "description": "O berço da F1, apresenta curvas rápidas de alta velocidade, extremamente desafiador",
                "elevation_change": 15.0,
                "is_active": True
            },
            {
                "name": "Suzuka",
                "country": "Japan",
                "city": "Suzuka",
                "lap_distance": 5.807,
                "total_laps": 53,
                "total_distance": 307.471,
                "base_lap_time": 89.0,
                "track_record": 87.319,
                "record_holder": "Lewis Hamilton",
                "record_year": 2019,
                "tire_wear_factor": 1.05,
                "fuel_effect": 0.031,
                "pit_loss_time": 21.0,
                "number_of_turns": 18,
                "longest_straight": 650,
                "drs_zones": 2,
                "track_type": "permanent",
                "direction": "clockwise",
                "typical_temp": 23.0,
                "rain_probability": 0.25,
                "first_grand_prix": 1987,
                "description": "O santuário japonês da velocidade. Um traçado técnico em '8' que desafia a física e separa os pilotos das lendas.",
                "elevation_change": 42.0,
                "is_active": True
            },
            {
                "name": "Interlagos",
                "country": "Brazil",
                "city": "São Paulo",
                "lap_distance": 4.309,
                "total_laps": 71,
                "total_distance": 305.909,
                "base_lap_time": 70.0,
                "track_record": 69.190,
                "record_holder": "Valtteri Bottas",
                "record_year": 2018,
                "tire_wear_factor": 1.0,
                "fuel_effect": 0.030,
                "pit_loss_time": 20.0,
                "number_of_turns": 15,
                "longest_straight": 820,
                "drs_zones": 2,
                "track_type": "permanent",
                "direction": "anti-clockwise",
                "typical_temp": 26.0,
                "rain_probability": 0.30,
                "first_grand_prix": 1973,
                "description": "Um dos templos da velocidade, Circuito apaixonante e completo que varia das curvas lentas, ondulações, e a subida da reta",
                "elevation_change": 40.0,
                "is_active": True
            }
        ]
        
        for circuit_data in circuits_data:
            circuit = Circuit(**circuit_data)
            db.add(circuit)
            print(f" ✓ {circuit.name}, {circuit.country}")
            
        db.commit()
        print(f" - {len(circuits_data)} circuitos criados!\n")
        
    
    
def seed_database():
    # Função principal para popular o banco
        
    print("\n" + "="*60)
    print(" F1 STRATEGY SIMULATOR - DATABASE SEEDING")
    print("="*60 + "\n")
        
    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print(" - Tabelas Criadas!\n")
        
    db = SessionLocal()
        
    try:
        create_tire_compounds(db)
        create_circuits(db)
            
        print("="*60)
        print(" - DATABASE SEEDING COMPLETO!")
        print("="*60)
        print("\nResumo:")
            
        tire_count = db.query(TireCompound).count()
        circuit_count = db.query(Circuit).count()
            
        print(f" 1. Compostos de pneus: {tire_count}")
        print(f" 2. Circuitos: {circuit_count}")
        print(f" - Banco pronto para uso!")
            
    except Exception as e:
        print(f"\n Erro ao popular banco: {e}")
        db.rollback()
        raise
    finally:
        db.close()
            
            
if __name__ == "__main__":
    seed_database()
            
            