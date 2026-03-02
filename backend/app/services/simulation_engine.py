# Motor Principal de Simulação de Corrida de F1

import random
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from app.models.circuit import Circuit
from app.models.tire_compound import TireCompound
from app.models.strategy import Strategy
from app.core.config import SimulationConstants


@dataclass
class LapResult:
    # Resultado de uma volta individual
    
    lap_number: int
    lap_time:float
    tire_compound: str
    tire_age: int
    tire_degradation: float
    fuel_load: float
    fuel_effect: float
    grip_level: float
    is_pit_lap: bool = False
    pit_time_loss: float = 0.0
    temperature: float = 25.0
    notes: str = ""
    

class RaceSimulationEngine:
    # Motor de simulação de corrida
    
    def __init__(
        self,
        circuit : Circuit,
        strategy: Strategy,
        tire_compounds: Dict[str, TireCompound],
        track_temperature: float = 25.0,
        random_seed: Optional[int] = None
    ):
        
        # Inicializa o motor de simulação
        
        self.circuit = circuit
        self.strategy = strategy
        self.tire_compounds = tire_compounds
        self.track_temperature = track_temperature
        
        if random_seed:
            random.seed(random_seed)
            
        
        self.current_lap = 0
        self.current_fuel = SimulationConstants.INITIAL_FUEL_LOAD
        self.current_tire_age = 0
        self.current_compound = None
        self.pit_stops_completed = []
        self.lap_results: List[LapResult] = []
        
        self.planned_pit_stops = self._parse_pit_stops()
        
    
    def planned_pit_stops(self) -> List[Dict]:
        # Extrai e ordena pit stops da estratégia
        
        if not self.strategy.strategy_data or "pit_stops" not in self.strategy.strategy_data:
            return []
        
        pit_stops = self.strategy.strategy_data["pit_stops"]
        return sorted(pit_stops, key=lambda x: x["lap"])
    
    
    def _get_tire_compound(self, compound_name: str) -> TireCompound:
        # Obtém objeto TireCompound pelo nome
        
        return self.tire_compounds.get(compound_name)
    
    
    def _calculate_base_lap_time(self) -> float:
        return self.circuit.base_lap_time
    
    
    def _calculate_tire_degradation(self, compound: TireCompound, age: int) -> float:
        # Calcula degradação de pneu com modelo não-linear
        
        base_degradation = compound.degradation_rate * age * self.circuit.tire_wear_factor
        
        # Cliff effect
        if age > compound.cliff_lap:
            laps_over_cliff = age - compound.cliff_lap
            cliff_penalty = compound.degradation_rate * laps_over_cliff * compound.cliff_factor
            base_degradation += cliff_penalty
            
        return base_degradation
    
    
    def _calculate_fuel_effect(self, fuel_kg: float) -> float:
        # Calcula impacto do combustível no tempo da volta
        # Regra: 0.03s por kg de combustível
        
        return fuel_kg * self.circuit.fuel_effect
    
    
    def _calculate_temperature_effect(self, compound: TireCompound) -> float:
        # Calcula impacto da temperatura no grip
        # Retorno: (1.0 = ótimo, maior que 1.0 = mais lento)
        
        optimal_temperature = (compound.optimal_temp_min + compound.optimal_temp_max) / 2
        
        temperature_diference = abs(self.track_temperature - optimal_temperature)
        
        # Penalidade de 0.2% por grau fora do ótimo
        if temperature_diference > 0:
            penalty = temperature_diference * SimulationConstants.TEMP_IMPACT_FACTOR
            return 1 + penalty
        
        return 1.0
    
    
    def _calculate_warm_up_penalty(self, compound: TireCompound, age: int) -> float:
        # Calcula a penalidade do aquecimento dos pneus nas voltas de aquecimento
        
        if age <= compound.warm_up_laps:
            return  compound.warm_up_penalty * (compound.warm_up_laps - age + 1)
        return 0.0
    
    
    def _add_realistic_variance(self) -> float:
        # Adiciona variação aleátoria a simulação
        # Pilotos não fazem voltas idênticas, há sempre pequenas variações
        
        return random.uniform(
            -SimulationConstants.LAP_TIME_VARIATION,
            SimulationConstants.LAP_TIME_VARIATION
        )
        
        
    def _is_pit_lap(self, lap: int) -> Tuple[bool, Optional[Dict]]:
        
        for pit_stop in self.planned_pit_stops:
            if pit_stop["lap"] == lap:
                return True, pit_stop
        return False, None
    
    
    def _execute_pit_stop(self, pit_stop: Dict) -> float:
        
        pit_duration = pit_stop.get("duration", random.uniform(2.0, 3.0))
        
        pit_loss = self.circuit.pit_loss_time
        
        new_compound_name = pit_stop["compound"]
        self.current_compound = new_compound_name
        self.current_tire_age = 0
        
        self.pit_stops_completed.append({
            "lap": self.current_lap,
            "compound": self.current_compound,
            "duration": pit_duration,
            "total_loss": pit_duration + pit_loss
        })
        
        return pit_duration + pit_loss
    
    
    def simulate_lap(self, lap: int) -> LapResult:
        
        self.current_lap = lap
        
        is_pit, pit_data = self._is_pit_lap(lap)
        pit_time_loss = 0.0
        
        if self.current_compound is None:
            if self.planned_pit_stops:
                self.current_compound = self.planned_pit_stops[0]["compound"]
            else:
                self.current_compound = "C3"
                
        
        compound = self._get_tire_compound(self.current_compound)
        if not compound:
            raise ValueError(f"Composto '{self.current_compound}' não encontrado!")
        
        
        # Cálculo do temp de volta
        
        lap_time = self._calculate_base_lap_time()
        
        grip_multiplier = compound.grip_multiplier(self.track_temperature)
        base_grip_effect = (1.0 - compound.base_grip) * 2
        lap_time += base_grip_effect
        
        tire_degradation = self._calculate_tire_degradation(compound, self.current_tire_age)
        lap_time += tire_degradation
        
        warm_up_penalty = self._calculate_warm_up_penalty(compound, self.current_tire_age)
        lap_time += warm_up_penalty
        
        fuel_effect = self._calculate_fuel_effect(self.current_fuel)
        lap_time += fuel_effect
        
        temperature_multiplier = self._calculate_temperature_effect(compound)
        lap_time += temperature_multiplier
        
        lap_time += self._add_realistic_variance()
        
        
        if is_pit:
            pit_time_loss = self._execute_pit_stop(pit_data)
            lap_time += pit_time_loss
        
        
        self.current_tire_age += 1
        self.current_fuel -= SimulationConstants.FUEL_COMSUMPTION_PER_LAP
        
        result = LapResult(
            lap_number=lap,
            lap_time=lap_time,
            tire_compound=self.current_compound,
            tire_age=self.current_tire_age,
            tire_degradation=tire_degradation,
            fuel_load=self.current_fuel,
            fuel_effect=fuel_effect,
            grip_level=grip_multiplier,
            is_pit_lap=is_pit,
            pit_time_loss=pit_time_loss,
            temperature=self.track_temperature
        )
        
        self.lap_results.append(result)
        return result
    
    
    def simulate_race(self) -> Dict:
        # Simula a corrida completa
        
        print(f"\n1. Iniciando simulação: {self.strategy.name}")
        print(f"- Circuito: {self.circuit.name}")
        print(f"- Voltas: {self.circuit.total_laps}")
        print(f"- Pit Stops planejados: {len(self.planned_pit_stops)}")
        
        # Resetar estado
        self.lap_results = []
        self.pit_stops_completed = []
        self.current_lap = 0
        self.current_fuel = SimulationConstants.INITIAL_FUEL_LOAD
        self.current_tire_age = 0
        self.current_compound =  None
        
        for lap in range(1, self.circuit.total_laps + 1):
            result = self.simulate_lap(lap)
            
            if lap % 10 == 0 or result.is_pit_lap:
                status = "PIT!" if result.is_pit_lap else "✓"
                print(f" Volta {lap:2d}: {result.lap_time:.3f}s [{result.tire_compound}] {status}")
                
        return self._generate_results()
        
        
    def _generate_results(self) -> Dict:
            
        if not self.lap_results:
            return {}
        
        lap_times = [race.lap_time for race in self.lap_results]
        
        total_time = sum(lap_times)
        average_lap = sum(lap_times) / len(lap_times)
        fastest_lap = min(lap_times)
        fastest_lap_num = lap_times.index(fastest_lap) + 1
        slowest_lap = max(lap_times)
        
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60) 
        seconds = total_time % 60
        formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
        
        total_pit_time = sum([pit["total_loss"] for pit in self.pit_stops_completed])
        
        results = {
            "total_race_time": total_time,
            "total_race_time_formatted": formatted_time,
            "average_lap_time": average_lap,
            "fastest_lap": fastest_lap,
            "fastest_lap_number": fastest_lap_num,
            "slowest_lap": slowest_lap,
            "total_pit_stops": len(self.pit_stops_completed),
            "total_pit_time": total_pit_time,
            "fuel_used": SimulationConstants.INITIAL_FUEL_LOAD - self.current_fuel,
            "lap_by_lap": [
                {
                    "lap": race.lap_number,
                    "time": race.lap_time,
                    "compound": race.tire_compound,
                    "tire_age": race.tire_age,
                    "is_pit": race.is_pit_lap
                }
                for race in self.lap_results
            ],
            "pit_stops": self.pit_stops_completed
        }
        
        print(f"\n{'='*60}")
        print(f"2. RESULTADOS DA SIMULAÇÃO")
        print(f"{'='*60}")
        print(f"- Tempo Total: {formatted_time}")
        print(f"- Tempo Médio: {average_lap:.3f}s")
        print(f"- Volta mais Rápida: {fastest_lap:.3f}s (Volta {fastest_lap_num})")
        print(f"- Tempo nos Boxes: {total_pit_time:.1f}s ({len(self.pit_stops_completed)} paradas)")
        print(f" Combustível Usado: {results['fuel_used']:.1f}kg")
        print(f"{'='*60}\n")
        
        return results
    

# Funções Auxiliares

def compare_strategies(
    circuit: Circuit,
    strategies: List[Strategy],
    tire_compounds: Dict[str, TireCompound]
) -> Dict:
    
    results = []
    
    for strategy in strategies:
        engine = RaceSimulationEngine(circuit, strategy, tire_compounds)
        result = engine.simulate_race()
        result['strategy_name'] = strategy.name
        results.append(result)
        
    results.sort(key=lambda x: x["total_race_time"])
    
    if results:
        results[0]["is_fastest"] = True
        
    return {
        "strategies_compared": len(results),
        "results": results,
        "best_strategy": results[0]["strategy_name"] if results else None,
        "time_difference": results[-1]["total_race_time"] - results[0]["total_race_time"] if len(results) > 1 else 0 
    }