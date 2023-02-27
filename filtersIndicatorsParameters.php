//В этом файле собраны фильтры и индикаторы, которые исползуем у нас в софте.  
//Они же прописаны в описании системы в разделе индикаторов
//при разработке системы, нужно использовать именно эти функции. 


//Базовый уровень по 15м-свечам (15м-график, уровень глубины сделки в проценте)
function getOrderPriceByOHLCV($ohlcv, $priceMinusPerc, $levelCandle=null){
	if(is_null($levelCandle))$levelCandle = 3;

	if(sizeof($ohlcv)==0){
		return array(false, false, "No ohlcv.", -1);
	}
	elseif($ohlcv[0][1]==null){
		return array(false, false, "No ohlcv.", -1);
	}

	$timeFrame = 15*60; //таймфрейм графика - 15-минутка

	//12 часовой отрезок берем на графике для анализа
	$timeBack = 12*60*60; //ВАЖНО!!! Если менять этот параметр, то нужно переписывать блок с углами наклона графика!!!


	$legPerc = 10; //10% шаг для распределения всего графика
	$legOffset = 2/3; //смещение для определения второго распределения графика

	if(!isset($priceMinusPerc))$priceMinusPerc = 25; //Минус сколько процентов от уровня - ставить цену ордера

	$percMaxDiffer = 10; //10% максимальный процент за 12 часов, чтобы градус был приемлемым. Иначе убираем урдер

	//Определение уровней, настройки
	$mainLevelComparation = 200; //на сколько процентов минимум должен отличаться уровень главный, при наличии несокльких

	$timeBackGraph = (time()-$timeBack)*1000;

	//Если в начале графика нет 3 свечи и далее - достраиваем (2-я свч)
	$nowMinutes = date("i");
	if($nowMinutes>=0 && $nowMinutes<15)$candleStartMinutes = 0;
	elseif($nowMinutes>=15 && $nowMinutes<30)$candleStartMinutes = 15;
	elseif($nowMinutes>=30 && $nowMinutes<45)$candleStartMinutes = 30;
	elseif($nowMinutes>=45 && $nowMinutes<=59)$candleStartMinutes = 45;
	$timeToCompare = mktime(date("H"), $candleStartMinutes, 0, date("n"), date("j"), date("Y"));
	$candle3rdTime = ($timeToCompare-$timeFrame*2)*1000;

	//дорабатываем график (отсутствующие свечи, и тд)
	$ohlcv = buildFullOhlcv($ohlcv);
	$maxGraph = 0;
	$minGraph = 0;

	//находим минимум и максимум графика и обрезаем
	for($i=0; $i<sizeof($ohlcv); $i++){
		$ohlcvEl = $ohlcv[$i];
		if($ohlcvEl[0]<$timeBackGraph)break;

		$openPrice = $ohlcvEl[1];
		$closePrice = $ohlcvEl[4];

		if($maxGraph<$closePrice)$maxGraph = $closePrice;
		if($minGraph==0)$minGraph = $closePrice;
		elseif($minGraph>$closePrice)$minGraph = $closePrice;
	}


	//print_r($ohlcv);

	//Делим график по оси Y на периоды по $legPerc процентов
	$graphPeriods1 = array($minGraph);

	$graphPeriods2 = array($minGraph);
	$plusPeriod2 = round(($minGraph/100) * round($legPerc*$legOffset, 1), 10);
	$nextPeriod2 = $graphPeriods2[0]+$plusPeriod2;
	if( $nextPeriod2 < $maxGraph )$graphPeriods2[] = $nextPeriod2;

	$plusPeriod = round(($minGraph/100) * $legPerc, 10);


	while($graphPeriods1[sizeof($graphPeriods1)-1]<$maxGraph){
		$currentPeriod1 = $graphPeriods1[sizeof($graphPeriods1)-1];
		$currentPeriod2 = $graphPeriods2[sizeof($graphPeriods2)-1];

		$nextPeriod1 = $currentPeriod1+$plusPeriod;
		$nextPeriod2 = $currentPeriod2+$plusPeriod;

		if($nextPeriod1>$maxGraph)$nextPeriod1 = $maxGraph;
		$graphPeriods1[] = $nextPeriod1;

		if($nextPeriod2>$maxGraph){
			if(!isset($period2Done)){

				$period2Done = true;
				$graphPeriods2[] = $maxGraph;
			}
		}
		else {
			$graphPeriods2[] = $nextPeriod2;
		}

	}
	if(sizeof($graphPeriods1)==1)$graphPeriods1[] = $maxGraph;
	if(sizeof($graphPeriods2)==1)$graphPeriods2[] = $maxGraph;


	$graphPeriodsStat1 = array();
	for($i=0; $i<(sizeof($graphPeriods1)-1); $i++){
		$level = array(sprintf('%.10f',$graphPeriods1[$i]), sprintf('%.10f',$graphPeriods1[$i+1]), 0, array());
		$graphPeriodsStat1[] = $level;

	}

	$graphPeriodsStat2 = array();
	for($i=0; $i<(sizeof($graphPeriods2)-1); $i++){
		$graphPeriodsStat2[] = array(sprintf('%.10f',$graphPeriods2[$i]), sprintf('%.10f',$graphPeriods2[$i+1]), 0, array());
	}



	//Распределяем каждую точку графика (закрытие свечи) по периодам, подсчитываем общее кол-во в каждом периоде
	$graphTimeScale2 = array();
	$graphTimeScale1 = array();
	$y1=0;
	$y2=0;

	$graphSize1 = sizeof($graphPeriodsStat1);
	$graphSize2 = sizeof($graphPeriodsStat2);


	foreach($ohlcv as $ohlcvEl){
		if($ohlcvEl[0]<$timeBackGraph)break;

		$closePrice = $ohlcvEl[4];

		//для первого распределения графика
		for($i=0; $i<$graphSize1; $i++){

			if(!isset($graphPeriodsStat1[$i+1][1])){
				if($closePrice<=$graphPeriodsStat1[$i][1])$scndCond = true;
				else $scndCond = false;

			}
			else {

				if($closePrice<$graphPeriodsStat1[$i][1])$scndCond = true;
				else $scndCond = false;
			}

			if($closePrice>=$graphPeriodsStat1[$i][0] && $scndCond){
				//Общие данные по уровням
				$graphPeriodsStat1[$i][2]++;
				$graphPeriodsStat1[$i][3][] = sprintf('%.10f',$closePrice);

				//Заполняем данные по уровням по временной шкале
				if(isset($prevPeriod1))if($prevPeriod1!=$i){
					$y1++;
				}
				$prevPeriod1 = $i;
				if(!isset($graphTimeScale1[$y1])){
					$graphTimeScale1[$y1] = array($graphPeriodsStat1[$i][0], $graphPeriodsStat1[$i][1], 1, array(sprintf('%.10f',$closePrice)), $i);
				}
				else {
					$graphTimeScale1[$y1][2]++;
					$graphTimeScale1[$y1][3][] = sprintf('%.10f',$closePrice);
				}

				break 1;
			}
		}

		//для второго распределения графика
		for($i=0; $i<$graphSize2; $i++){

			if(!isset($graphPeriodsStat2[$i+1][1])){
				if($closePrice<=$graphPeriodsStat2[$i][1])$scndCond = true;
				else $scndCond = false;

			}
			else {

				if($closePrice<$graphPeriodsStat2[$i][1])$scndCond = true;
				else $scndCond = false;
			}

			if($closePrice>=$graphPeriodsStat2[$i][0] && $scndCond){
				//Общие данные по уровням
				$graphPeriodsStat2[$i][2]++;
				$graphPeriodsStat2[$i][3][] = sprintf('%.10f',$closePrice);

				//Заполняем данные по уровням по временной шкале
				if(isset($prevPeriod2))if($prevPeriod2!=$i){
					$y2++;
				}
				$prevPeriod2 = $i;
				if(!isset($graphTimeScale2[$y2])){
					$graphTimeScale2[$y2] = array($graphPeriodsStat2[$i][0], $graphPeriodsStat2[$i][1], 1, array(sprintf('%.10f',$closePrice)), $i);
				}
				else {
					$graphTimeScale2[$y2][2]++;
					$graphTimeScale2[$y2][3][] = sprintf('%.10f',$closePrice);
				}

				break 1;
			}
		}
	}


	//Определяем наиболее лучшее распределение по уровням
	$maxLevel1 = array();
	$maxLevel2 = array();
	foreach($graphPeriodsStat1 as $graphPeriodsStat1El){
		if(sizeof($maxLevel1)==0)$maxLevel1 = $graphPeriodsStat1El;
		else {
			if($maxLevel1[2]<$graphPeriodsStat1El[2])$maxLevel1 = $graphPeriodsStat1El;
		}
	}
	foreach($graphPeriodsStat2 as $graphPeriodsStat2El){
		if(sizeof($maxLevel2)==0)$maxLevel2 = $graphPeriodsStat2El;
		else {
			if($maxLevel2[2]<$graphPeriodsStat2El[2])$maxLevel2 = $graphPeriodsStat2El;
		}
	}

	//Какой вариант победил выбираем
	if($maxLevel1[2]>$maxLevel2[2]){
		$graphPeriodsStat = $graphPeriodsStat1;
		$graphTimeScale = $graphTimeScale1;
	}
	else {
		$graphPeriodsStat = $graphPeriodsStat2;
		$graphTimeScale = $graphTimeScale2;
	}




	//если уровней больше чем один
	if(sizeof($graphPeriodsStat)!=1){
		//определяем главный уровень по временной шкале
		$maxLevelScale = array();
		foreach($graphTimeScale as $graphTimeScaleEl){
			if(sizeof($maxLevelScale)==0)$maxLevelScale = $graphTimeScaleEl;
			else {
				if($maxLevelScale[2]<$graphTimeScaleEl[2])$maxLevelScale = $graphTimeScaleEl;
			}
		}

		//определяем процентное соотношение каждого уровня от главного уровня + удаляем незначительные уровни
		$percMinLevel = 30;//минимальный порог процента, чтобы уровень был значимым
		$newGraphTimeScale = array();

		for($i=0; $i<sizeof($graphTimeScale); $i++){
			$graphTimeScaleEl = $graphTimeScale[$i];
			$perc = round(($graphTimeScaleEl[2]*100)/$maxLevelScale[2], 2);
			$graphTimeScale[$i][5] = $perc;

			//Первые и последние группы свечей  всегда добавляем
			if(sizeof($newGraphTimeScale)==0 || $i==(sizeof($graphTimeScale)-1)){
				if(sizeof($newGraphTimeScale)==0)$newGraphTimeScale[] = $graphTimeScale[$i];
				else {
					//если уровни предыдущий и текущий сходятся - просто совмещаем их
					if($newGraphTimeScale[sizeof($newGraphTimeScale)-1][4]==$graphTimeScale[$i][4]){
						$newGraphTimeScale[sizeof($newGraphTimeScale)-1][2]+=$graphTimeScale[$i][2];
						$newGraphTimeScale[sizeof($newGraphTimeScale)-1][3] = array_merge($newGraphTimeScale[sizeof($newGraphTimeScale)-1][3], $graphTimeScale[$i][3]);
					}
					else $newGraphTimeScale[] = $graphTimeScale[$i];
				}
			}
			//Если разница по уровням с соседним больше чем 1, тоже добавляем, сколько бы ни было там свечей
			elseif($newGraphTimeScale[sizeof($newGraphTimeScale)-1][4]+2 <= $graphTimeScale[$i][4] || $newGraphTimeScale[sizeof($newGraphTimeScale)-1][4]-2 >= $graphTimeScale[$i][4]){
				$newGraphTimeScale[] = $graphTimeScale[$i];
			}
			//если процент подходит - добавляем
			elseif($perc>=$percMinLevel){
					//если уровни предыдущий и текущий сходятся - просто совмещаем их
					if($newGraphTimeScale[sizeof($newGraphTimeScale)-1][4]==$graphTimeScale[$i][4]){
						$newGraphTimeScale[sizeof($newGraphTimeScale)-1][2]+=$graphTimeScale[$i][2];
						$newGraphTimeScale[sizeof($newGraphTimeScale)-1][3] = array_merge($newGraphTimeScale[sizeof($newGraphTimeScale)-1][3], $graphTimeScale[$i][3]);
					}
					else $newGraphTimeScale[] = $graphTimeScale[$i];
			}
		}

		$cleanedGraphTimeScale = $newGraphTimeScale;
	}


	//определяем цену закрытия 3-ей свечи
	if($levelCandle==2)$candle2ndTime = ($timeToCompare)*1000;
	else $candle2ndTime = ($timeToCompare-$timeFrame)*1000;


	foreach($ohlcv as $ohlcvEl){
		if($ohlcvEl[0]<$candle2ndTime){
			$candle3 = $ohlcvEl;
			if(sizeof($graphPeriodsStat)==1)$candle3LEvel = 0;
			else {
				for($i=0; $i<sizeof($graphPeriodsStat); $i++){

					if(!isset($graphPeriodsStat[$i+1][1])){
						if($candle3[4]<=$graphPeriodsStat[$i][1])$scndCond = true;
						else $scndCond = false;

					}
					else {
						if($candle3[4]<$graphPeriodsStat[$i][1])$scndCond = true;
						else $scndCond = false;
					}

					if($candle3[4]>=$graphPeriodsStat[$i][0] && $scndCond){
						$candle3LEvel = $i;
						break 1;
					}
				}
			}

			break;
		}
	}




	$OHLCVscenario = '';
	//если уровень только один
	if(sizeof($graphPeriodsStat)==1){
		if(!isset($candle3)){
			$return = array(false, false, "No 3rd candle", -1);
		}
		else {
			//$setPrice = ($candle3[4]/100) * (100-$priceMinusPerc);
			$setPrice = ($candle3[4]/(100+$priceMinusPerc)) * 100;
			$return = array(sprintf('%.10f',$candle3[4]), sprintf('%.10f',$setPrice), "Only 1 level", 1);
		}
	}
	//если уровней несоклько
	else {

		//Определяем, есть ли главный уровень
		$mainLevel = array();
		for($i=0; $i<sizeof($graphPeriodsStat); $i++){
			$periodEl = $graphPeriodsStat[$i];

			for($y=0; $y<sizeof($graphPeriodsStat); $y++){
				if($i==$y)continue 1;//пропускем если одинаковые периоды

				$comparePeriodEl = $graphPeriodsStat[$y];
				//Если 0 свечей в периоде
				if($comparePeriodEl[2]==0){
					continue 1;
				}

				$perc = ($periodEl[2]/$comparePeriodEl[2])*100;

				//Если хотябы один другой уровень будет не в два раза больше, то текущий уровень $periodEl - не является главным
				if($perc < $mainLevelComparation){
					continue 2;
				}
			}

			$mainLevel[] = array($i, $periodEl);
		}


		//Если есть главный уровень
		if(sizeof($mainLevel)>0){
			//print "Main level detected: ";
			//print_r($mainLevel);


			//Если уровень третьей свечи и главного уровня совпадают, то можно смело по 3 свече ставить цены
			if($mainLevel[0][0]==$candle3LEvel){
				//$setPrice = ($candle3[4]/100) * (100-$priceMinusPerc);
				$setPrice = ($candle3[4]/(100+$priceMinusPerc)) * 100;
				$return = array(sprintf('%.10f',$candle3[4]), sprintf('%.10f',$setPrice), "Several Levels. Main Level detected. 3rd candle = Main Level. Price = 3rd candle.", 2);
			}
			//Если уровень третьей свечи и нлавного уровня не совпадают
			else {
				//Если третья свеча вниз уходит, то опять по 3 свече ставим цену
				if($candle3LEvel<$mainLevel[0][0]){
					//$setPrice = ($candle3[4]/100) * (100-$priceMinusPerc);
					$setPrice = ($candle3[4]/(100+$priceMinusPerc)) * 100;
					$return = array(sprintf('%.10f',$candle3[4]), sprintf('%.10f',$setPrice), "Several Levels. Main Level detected. 3rd candle < Main Level. Price = 3rd candle.", 3);
				}
				//если вверх ушла 3 свеча от главного уровня - цену ставим относительно главного уровня
				else {

					//высчитываем среднюю арифм цену
					$sum = 0;
					foreach($mainLevel[0][1][3] as $mainLevelEl){
						$sum += $mainLevelEl;
					}
					$middleSum = round($sum/$mainLevel[0][1][2], 10);

					//$setPrice = ($middleSum/100) * (100-$priceMinusPerc);
					$setPrice = ($middleSum/(100+$priceMinusPerc)) * 100;
					$return = array(sprintf('%.10f',$middleSum), sprintf('%.10f',$setPrice), "Several Levels. Main Level detected. 3rd candle > Main Level. Price = Main Level.", 4);
				}

			}

		}
		//Если главного уровня нет, а есть просто преобладающие
		else {

			//$firstCandle = $cleanedGraphTimeScale[0];
			$lastCandle = $cleanedGraphTimeScale[sizeof($cleanedGraphTimeScale)-1];


			//Если уровни начала и 3 свечи разные - граик либо растет либо падает
			if($candle3LEvel!=$lastCandle[4]){
				//Если падает, то по третьей свече ставим цены
				if($candle3LEvel<$lastCandle[4]){
					//$setPrice = ($candle3[4]/100) * (100-$priceMinusPerc);
					$setPrice = ($candle3[4]/(100+$priceMinusPerc)) * 100;
					$return = array(sprintf('%.10f',$candle3[4]), sprintf('%.10f',$setPrice), "Several Levels. No Main Level. 3rd Candle < Last Candle: falling grahp. Price = 3rd candle.", 5);
				}
				//если растет
				else {
					//Определяем угол наклона.
					$procDiffer = ($candle3[4]*100)/$lastCandle[3][0]-100;

					//если сликшом большой угол наклона за 12 часов - то убираем ордер
					if($procDiffer>$percMaxDiffer){
						//print "NOOOOO";
						$return = array(false, false, "Several Levels. No Main Level. 3rd Candle > Last Candle: rising grahp. Angle too high. Delete Order. Wait..", 0);
					}
					//если допустимый, то цену ордера выбираем от третьей свечи
					else {
						//print "Допустимый угол наклона!";

						//$setPrice = ($candle3[4]/100) * (100-$priceMinusPerc);
						$setPrice = ($candle3[4]/(100+$priceMinusPerc)) * 100;
						$return = array(sprintf('%.10f',$candle3[4]), sprintf('%.10f',$setPrice), "Several Levels. No Main Level. 3rd Candle > Last Candle: rising grahp. Acceptable angle. Price = 3rd candle.", 6);
					}



				}
			}
			//Если одинаковые уровни
			else {
				//$setPrice = ($candle3[4]/100) * (100-$priceMinusPerc);
				$setPrice = ($candle3[4]/(100+$priceMinusPerc)) * 100;
				$return = array(sprintf('%.10f',$candle3[4]), sprintf('%.10f',$setPrice),  "Several Levels. No Main Level. 3rd Candle = Last Candle. Price = 3rd candle.", 7);
			}



		}
	}

	if(!isset($return))$return = array(false, false, "No pattern founded.", -1);

	return $return;
}



//Построение графика по торгам

function tradesToOHLCV($trades, $time){
	if (!isset($time))$time = '15m';
	$trades = cleanTrades($trades);

	if($time=='15m'){
		$nowMinutes = date("i", $trades[0]['timestamp']/1000);
		if($nowMinutes>=0 && $nowMinutes<15)$candleStartMinutes = 0;
		elseif($nowMinutes>=15 && $nowMinutes<30)$candleStartMinutes = 15;
		elseif($nowMinutes>=30 && $nowMinutes<45)$candleStartMinutes = 30;
		elseif($nowMinutes>=45 && $nowMinutes<=59)$candleStartMinutes = 45;
		$timeToCompare = mktime(date("H", $trades[0]['timestamp']/1000), $candleStartMinutes, 0, date("n", $trades[0]['timestamp']/1000), date("j", $trades[0]['timestamp']/1000), date("Y", $trades[0]['timestamp']/1000))*1000;

		$timeframe = 15*60*1000;
	}
	elseif($time=='1m'){
		$candleStartMinutes = date("i", $trades[0]['timestamp']/1000);
		$timeToCompare = mktime(date("H", $trades[0]['timestamp']/1000), $candleStartMinutes, 0, date("n", $trades[0]['timestamp']/1000), date("j", $trades[0]['timestamp']/1000), date("Y", $trades[0]['timestamp']/1000))*1000;

		$timeframe = 60*1000;
	}




	$candles = array();
	$i = 0;

	//foreach($trades as $tradesEl){
	$sizeofTrades = sizeof($trades);
	for($p=0; $p<$sizeofTrades; $p++){
		$tradesEl = $trades[$p];

		//Добавляем в эту свечу
		if($tradesEl['timestamp']>=$timeToCompare && $tradesEl['timestamp']<($timeToCompare+$timeframe)){

			if(!isset($candles[$i])){
				$candles[$i] = array($timeToCompare, $tradesEl['price'], $tradesEl['price'], $tradesEl['price'], $tradesEl['price'], $tradesEl['amount']);
				//$candles[$i] = array($timeToCompare, $tradesEl['price'], $tradesEl['price'], $tradesEl['price'], $tradesEl['price'], $tradesEl['amount'], array($tradesEl));
			}
			else {
				if($tradesEl['price']>$candles[$i][2])$candles[$i][2] = $tradesEl['price']; //highest price
				if($tradesEl['price']<$candles[$i][3])$candles[$i][3] = $tradesEl['price']; //lowest price
				$candles[$i][4] = $tradesEl['price']; //обновляем цену закрытия
				$candles[$i][5]+=$tradesEl['amount']; //value
				//$candles[$i][6][] = $tradesEl;


			}
		}
		//новая свеча
		else{

			while($tradesEl['timestamp']>($timeToCompare+$timeframe)){
				//новая свеча
				$i++;
				$timeToCompare+=$timeframe;

				//Если трейд в этой новой свече
				if($tradesEl['timestamp']>=$timeToCompare && $tradesEl['timestamp']<($timeToCompare+$timeframe)){

					//$candles[$i] = array($timeToCompare, $tradesEl['price'], $tradesEl['price'], $tradesEl['price'], $tradesEl['price'], $tradesEl['amount'], array($tradesEl));
					$candles[$i] = array($timeToCompare, $tradesEl['price'], $tradesEl['price'], $tradesEl['price'], $tradesEl['price'], $tradesEl['amount']);

				}
				//если нет
				else {
					$candles[$i] = $candles[$i-1];
					$candles[$i][0] += $timeframe;
					$candles[$i][1] = $candles[$i][4];
					$candles[$i][2] = $candles[$i][4];
					$candles[$i][3] = $candles[$i][4];
					$candles[$i][5] = 0;
					//$candles[$i][6] = array();
				}

			}



		}


	}

	$candles = array_reverse($candles);
	unset($candles[sizeof($candles)-1]);
	$candles = array_reverse($candles);

	return $candles;
}



//упорядочивание торгов(для cryptopia в частности) в нужном порядке

function cleanTrades ($trades){
	$toClean = array();
	$toCleanSort = array();
	$toCleanIters = array();
	$sizeofTrades = sizeof($trades);

	for($i=0; $i<$sizeofTrades; $i++){
		if(sizeof($toClean)==0){
			$toClean[] = $trades[$i];
			$toCleanSort[] = $trades[$i]['price'];
			$toCleanIters[] = $i;
		}
		else {
			//если одинаковые, то заносим в row
			if($trades[$i-1]['timestamp']==$trades[$i]['timestamp'] && $trades[$i-1]['side']==$trades[$i]['side']){
				$toClean[] = $trades[$i];
				$toCleanSort[] = $trades[$i]['price'];
				$toCleanIters[] = $i;
			}
			//если разные
			else {
				//Если больше одной записи, то упорядочивание делаем
				if(sizeof($toClean)>1){

					if($toClean[0]['side']=='buy')array_multisort($toCleanSort, SORT_ASC, $toClean);
					else array_multisort($toCleanSort, SORT_DESC, $toClean);

					$m = 0;
					foreach($toCleanIters as $k){
						$trades[$k] = $toClean[$m];
						$m++;
					}
				}


				$toClean = array($trades[$i]);
				$toCleanSort = array($trades[$i]['price']);
				$toCleanIters = array($i);
			}
		}

	}

	return $trades;
}



//Достраиваем недостающие свечи, если в графике есть пробелы без свечей (на некоторых биржах отдают так графики, если на тех моментах времени не было торгов)
function buildFullOhlcv($ohlcv){
	$timeFrame = 15*60; //таймфрейм графика - 15-минутка

	$ohlcvNew = array();

	//Заполняем пропущенные свечи
	for($i=0; $i<sizeof($ohlcv); $i++){
		$ohlcvEl = $ohlcv[$i];
		if(isset($ohlcv[$i+1]))$ohlcvElNext = $ohlcv[$i+1];
		else $ohlcvElNext = false;

		//если хотябы одна цена равна нулю - значит свечи не было(не было продаж)..на kucoin так. Заполняем пропущенные свечи
		if($ohlcvEl[1]==0){
			//Если на первой свече нет свечи
			if(!isset($ohlcv[$i-1])){
				unset($ohlcv[$i]);
				continue 1;
			}
			$missedCandlePrev = $ohlcv[$i-1];
			$missedCandlePrev[0] += $timeFrame*1000;
			$missedCandlePrev[1] = $missedCandlePrev[4];
			$missedCandlePrev[2] = $missedCandlePrev[4];
			$missedCandlePrev[3] = $missedCandlePrev[4];
			$missedCandlePrev[5] = 0;

			$ohlcv[$i] = $missedCandlePrev;
			$ohlcvEl = $ohlcv[$i];
		}

		$ohlcvNew[] = $ohlcvEl;
		if($ohlcvElNext){
				$missedCandle = $ohlcvEl;
				$missedCandle[0] += $timeFrame*1000;
				$missedCandle[1] = $missedCandle[4];
				$missedCandle[2] = $missedCandle[4];
				$missedCandle[3] = $missedCandle[4];
				$missedCandle[5] = 0;

				while($ohlcvElNext[0]>$missedCandle[0]){
					$ohlcvNew[] = $missedCandle;
					$missedCandle[0] += $timeFrame*1000;
				}
		}

	}
	$ohlcv = array_reverse($ohlcvNew);


	//Если в начале графика нет 3 свечи и далее - достраиваем
	$nowMinutes = date("i");
	if($nowMinutes>=0 && $nowMinutes<15)$candleStartMinutes = 0;
	elseif($nowMinutes>=15 && $nowMinutes<30)$candleStartMinutes = 15;
	elseif($nowMinutes>=30 && $nowMinutes<45)$candleStartMinutes = 30;
	elseif($nowMinutes>=45 && $nowMinutes<=59)$candleStartMinutes = 45;
	$timeToCompare = mktime(date("H"), $candleStartMinutes, 0, date("n"), date("j"), date("Y"));
	$candle3rdTime = ($timeToCompare-$timeFrame*2)*1000;

	if($ohlcv[0][0]<$candle3rdTime){

		$lastCandle = $ohlcv[0];
		$lastCandle[0] += $timeFrame*1000;
		$lastCandle[1] = $lastCandle[4];
		$lastCandle[2] = $lastCandle[4];
		$lastCandle[3] = $lastCandle[4];
		$lastCandle[5] = 0;

		$ohlcv = array_reverse($ohlcv);

		while($candle3rdTime>=$lastCandle[0]){
			$ohlcv[] = $lastCandle;
			$lastCandle[0] += $timeFrame*1000;
		}

		$ohlcv = array_reverse($ohlcv);
	}


	return $ohlcv;
}



//рассчет уровня максимальной цены ордера по дневному графику (1d-PumpProtect level)
function pumpProtectorLowperc($ohlcv){
	$maxPercentAboveLevel = 0; //максимальный процент над самой низкой ценой закрытия свечи (из 3х). Цена ордера должна быть ниже этого

	$ohlcv = array_reverse($ohlcv);

	//$yesterDay = date("j", mktime(0, 0, 0, date("n"), date("j")-1, date("Y")));
	$yesterDay = date("j", $ohlcv[1][0]/1000);
	if(!isset($ohlcv[1])){
		//print_r($ohlcv);
	}

	$countCandles = 4;
	$countedCandles = -1;

	$lowestClosePrice = -1;

	foreach ($ohlcv as $ohlcvEl) {

		if(date("j", $ohlcvEl[0]/1000)==$yesterDay){
			$countedCandles=0;
		}


		if($countedCandles>=0){
			if($lowestClosePrice<0)$lowestClosePrice = $ohlcvEl[4];
			elseif($ohlcvEl[4]<$lowestClosePrice)$lowestClosePrice = $ohlcvEl[4];


			$countedCandles++;
			if($countedCandles>=$countCandles)break;
		}
	}

	if($lowestClosePrice<0)return false;

	$maxOrderPrice = round(((100+$maxPercentAboveLevel)/100)*$lowestClosePrice, 12);

	return array($lowestClosePrice, $maxOrderPrice);
}





//ф-ция конвертации графика из меньшего таймфрейма в больший
function convertOHLCVupdated($ohlcv, $newScale, $fromScale=null){
  $fromScale = is_null($fromScale)?'15m':$fromScale;


	if($newScale=='1D'){
		$timeToCompare = mktime(0, 0, 0, date("n", $ohlcv[0][0]/1000), date("j", $ohlcv[0][0]/1000), date("Y", $ohlcv[0][0]/1000))*1000;
		$timeFrame = 24*60*60*1000; //таймфрейм графика
	}
	elseif($newScale=='1h'){
		$timeToCompare = mktime(date("H", $ohlcv[0][0]/1000), 0, 0, date("n", $ohlcv[0][0]/1000), date("j", $ohlcv[0][0]/1000), date("Y", $ohlcv[0][0]/1000))*1000;
		$timeFrame = 60*60*1000; //таймфрейм графика
	}
	elseif($newScale=='2h'){
		$validHours = array(22, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2, 0);
		$validHour = date("H", $ohlcv[0][0]/1000);

		if(!in_array($validHour, $validHours)){
			foreach($validHours as $validHoursEl){

				if($validHour>$validHoursEl){
					$validHour = $validHoursEl;
					break 1;
				}

			}
		}


		$timeToCompare = mktime($validHour, 0, 0, date("n", $ohlcv[0][0]/1000), date("j", $ohlcv[0][0]/1000), date("Y", $ohlcv[0][0]/1000))*1000;
		$timeFrame = 2*60*60*1000; //таймфрейм графика
	}
	elseif($newScale=='4h'){
		$validHours = array(20, 16, 12, 8, 4, 0);
		$validHour = date("H", $ohlcv[0][0]/1000);

		if(!in_array($validHour, $validHours)){
			foreach($validHours as $validHoursEl){

				if($validHour>$validHoursEl){
					$validHour = $validHoursEl;
					break 1;
				}

			}
		}

		$timeToCompare = mktime($validHour, 0, 0, date("n", $ohlcv[0][0]/1000), date("j", $ohlcv[0][0]/1000), date("Y", $ohlcv[0][0]/1000))*1000;
		$timeFrame = 4*60*60*1000; //таймфрейм графика
	}
	elseif($newScale=='30m'){
		$cndlMinute = date("i", $ohlcv[0][0]/1000);
		$nowMinutes = ($cndlMinute>=0 && $cndlMinute<30)?0:30;
		$timeToCompare = mktime(date("H", $ohlcv[0][0]/1000), $nowMinutes, 0, date("n", $ohlcv[0][0]/1000), date("j", $ohlcv[0][0]/1000), date("Y", $ohlcv[0][0]/1000))*1000;
		$timeFrame = 30*60*1000; //таймфрейм графика
	}
  elseif($newScale=='15m'){
		$cndlMinute = date("i", $ohlcv[0][0]/1000);

    if($cndlMinute>=0 && $cndlMinute<15)$nowMinutes = 0;
    elseif($cndlMinute>=15 && $cndlMinute<30)$nowMinutes = 15;
    elseif($cndlMinute>=30 && $cndlMinute<45)$nowMinutes = 30;
    elseif($cndlMinute>=45 && $cndlMinute<60)$nowMinutes = 45;

		$timeToCompare = mktime(date("H", $ohlcv[0][0]/1000), $nowMinutes, 0, date("n", $ohlcv[0][0]/1000), date("j", $ohlcv[0][0]/1000), date("Y", $ohlcv[0][0]/1000))*1000;
		$timeFrame = 15*60*1000; //таймфрейм графика
	}
	else return false;

	//print $timeToCompare."<<";


	$newOhlcv = array();
	$value24 = 0;
	$openPrice = 0;
	$closePrice = 0;
	$minPrice = 0;
	$maxPrice = 0;

	$candles = array();

	for($i=0; $i<sizeof($ohlcv); $i++){
		$ohlcvEl = $ohlcv[$i];

		//если пошла следующая свеча
		if($ohlcvEl[0]<$timeToCompare){
			//print $i."-";

			//Закрываем предыдущую свечу
			$openPrice = $ohlcv[$i-1][1];
			//$newOhlcv[] = array($timeToCompare, $openPrice, $maxPrice, $minPrice, $value24, $candles);
			$newOhlcv[] = array($timeToCompare, $openPrice, $maxPrice, $minPrice, $closePrice, $value24);


			$candles = array();
			$candles[] = $ohlcvEl;

			//заносим данные по новой свече
			$value24 = $ohlcvEl[5];
			$closePrice = $ohlcvEl[4];
			$minPrice = $ohlcvEl[3];
			$maxPrice = $ohlcvEl[2];
			$openPrice = $ohlcvEl[1];
			$timeToCompare -= $timeFrame;
			//break;
		}
		else {
			//print $i."+";
			$candles[] = $ohlcv[$i];


			$value24 += $ohlcvEl[5];
			if($closePrice==0)$closePrice = $ohlcvEl[4];

			if($minPrice==0)$minPrice = $ohlcvEl[3];
			elseif($minPrice>$ohlcvEl[3])$minPrice = $ohlcvEl[3];

			if($maxPrice==0)$maxPrice = $ohlcvEl[2];
			elseif($maxPrice<$ohlcvEl[2])$maxPrice = $ohlcvEl[2];

			//if($openPrice==0)$openPrice = $ohlcvEl[1];

			//если последняя
			if($i==(sizeof($ohlcv)-1))$newOhlcv[] = array($timeToCompare, $ohlcvEl[1], $maxPrice, $minPrice, $closePrice, $value24);
		}
	}


	//unset($newOhlcv[(sizeof($newOhlcv)-1)]);

	return array_reverse($newOhlcv);
}




//ф-ция сортировки
function sort_by($array) {
    $arguments = func_get_args();
    $array = array_pop($arguments);
    $variables = array();
    foreach ($arguments as $index => $key) {
        $variables[] = '$arguments['.$index.']';
        if ($index % 2 == 0) {
            $arguments[$index] = array();
            foreach ($array as $row) $arguments[$index][] = $row[$key];
        }
    }
    // call_user_func_array will not work in this case
    eval('array_multisort('.implode(', ', $variables).', $array);');
    return $array;
}

function timems(){
	return round(microtime(true) * 1000);
}

function dateTag(){
	return date("d.m H:i:s.").substr(timems(), -3);
}



//RSI
function indicator_rsi($ohclv, $period, $offset=null){
  if($offset!=null)$offsetIter = $offset;
	else $offsetIter = 0;

  $osize = sizeof($ohclv);
  $uArray = array();
  $dArray = array();
  //$ohclv = array_reverse($ohclv);

  for($i=0; $i<$osize; $i++){


    $uIter = null;
    $dIter = null;

    if($i>0){
      $uIter = $ohclv[$i][4] - $ohclv[$i-1][4];
      if($uIter<0)$uIter = 0;
      $dIter = $ohclv[$i-1][4] - $ohclv[$i][4];
      if($dIter<0)$dIter = 0;
    }

    $uArray[] = $uIter;
    $dArray[] = $dIter;
  }

  $uArrayExp = exponentialParam($uArray, $period, 1);
  $dArrayExp = exponentialParam($dArray, $period, 1);

  $rsiArray = array();
  //
  for($i=0; $i<$osize; $i++){
		$rsiIter = null;

    if($i>=($offsetIter+$period-1+1)){
      if($dArrayExp[$i]==0)$rsiIter = 100;
      else {
        $rsIter = $uArrayExp[$i] / $dArrayExp[$i];
        $rsiIter = 100 - (100/(1 + $rsIter));
      }

      $rsiIter = round ($rsiIter, 1);

    }

    $rsiArray[] = $rsiIter;
  }

  return $rsiArray;
}


//RSI tradingview
function indicator_rsi_tv($ohclv, $period, $offset=null){
  if($offset!=null)$offsetIter = $offset;
	else $offsetIter = 0;

  $osize = sizeof($ohclv);
  $uArray = array();
  $dArray = array();
  //$ohclv = array_reverse($ohclv);

  for($i=0; $i<$osize; $i++){


    $uIter = null;
    $dIter = null;

    if($i>0){
      $uIter = $ohclv[$i][4] - $ohclv[$i-1][4];
      if($uIter<0)$uIter = 0;
      $dIter = $ohclv[$i-1][4] - $ohclv[$i][4];
      if($dIter<0)$dIter = 0;
    }

    $uArray[] = $uIter;
    $dArray[] = $dIter;
  }

  $uArrayExp = rollingParam($uArray, $period, 1);
  $dArrayExp = rollingParam($dArray, $period, 1);

  $rsiArray = array();
  //
  for($i=0; $i<$osize; $i++){
		$rsiIter = null;

    if($i>=($offsetIter+$period-1+1)){
      if($dArrayExp[$i]==0)$rsiIter = 100;
      else {
        $rsIter = $uArrayExp[$i] / $dArrayExp[$i];
        $rsiIter = 100 - (100/(1 + $rsIter));
      }

      $rsiIter = round ($rsiIter, 1);

    }

    $rsiArray[] = $rsiIter;
  }

  return $rsiArray;
}


//macd%
function indicator_macd($ohclv, $periodFast, $periodLong, $periodSignal, $type='percent', $offset=null){
	if($offset!=null)$offsetIter = $offset;
	else $offsetIter = 0;

  $osize = sizeof($ohclv);

	//делаем выборку только цен закрытия
	$closeArray = array();
	for($i=0; $i<$osize; $i++){
		$closeArray[] = $ohclv[$i][4];
	}

	$emaFast = exponentialParam($closeArray, $periodFast, $offset);
	$emaLong = exponentialParam($closeArray, $periodLong, $offset);

	$macd = array();
	$signalOffset = 0;
	for($i=0; $i<$osize; $i++){
		$macd[$i] = null;

		if($emaFast[$i]!==null && $emaLong[$i]!==null){
			$macd[$i] = $emaFast[$i] - $emaLong[$i];

			if($type=='percent'){

				$macd[$i] = round(($macd[$i]*100)/$emaLong[$i], 2);

			}
		}
		else {
			$signalOffset = $i+1;
		}

	}

	$macdSignal = exponentialParam($macd, $periodSignal, $signalOffset);

	$macdStolbs = array();

	for($i=0; $i<$osize; $i++){
		$macdStolbs[$i] = null;

		if($macdSignal[$i]!==null && $macd[$i]!==null){
			$macdSignal[$i] = round($macdSignal[$i], 2);
			$macdStolbs[$i] = $macd[$i] - $macdSignal[$i];
		}
	}

	return array('macd'=>$macd, 'signal'=>$macdSignal, 'stolbs'=>$macdStolbs);
}


//Aroon
function indicator_aroon($ohclv, $period){
	$ohlcvSize = sizeof($ohclv);
	//$ohclv = array_reverse($ohclv);


	for($i=0; $i<$ohlcvSize; $i++){
		$aroonIter = array(null, null);
		$aroonUpIter = null;
		$aroonDownIter = null;

		if($i>=($period-1)){

			$daysSinceHigh = 0;
			$daysSinceLow = 0;
			$lowest = 0;
			$highest = 0;

			for($y=($i-($period-1)); $y<=$i; $y++){


				if($lowest==0)$lowest = $ohclv[$y][3];
				elseif($ohclv[$y][3]<=$lowest){
					$lowest = $ohclv[$y][3];
					$daysSinceLow = 0;
				}
				else $daysSinceLow++;

				if($highest==0)$highest = $ohclv[$y][2];
				elseif($ohclv[$y][2]>=$highest){
					$highest = $ohclv[$y][2];
					$daysSinceHigh = 0;
				}
				else $daysSinceHigh++;

			}

			$aroonUpIter = round((($period-$daysSinceHigh)/$period)*100, 1);
			$aroonDownIter = round((($period-$daysSinceLow)/$period)*100, 1);
			$aroonIter = array($aroonUpIter, $aroonDownIter);
		}

		$aroonUp[] = $aroonUpIter;
		$aroonDown[] = $aroonDownIter;
		$aroon[] =$aroonIter;
	}


	//$aroonUpWma = waightedParam($aroonUp, 8, $period);
	//$aroonDownWma = waightedParam($aroonDown, 8, $period);

	//for($i=0; $i<$ohlcvSize; $i++){
	//	$aroon[$i][2] = $aroonUpWma[$i];
	//	$aroon[$i][3] = $aroonDownWma[$i];
	//}

	return ($aroon);
}


//полосы болинджера - ширина Bbands Width
function indicator_bbandsw($ohclv, $period, $multiplyer, $offset=null){
	$bbands = ohclv_bbands(array_reverse($ohclv), $period, $multiplyer, $offset=null);

//print_r($bbands);

	$bbandsw = array();
	foreach($bbands as $bbandsEl){
		if(is_null($bbandsEl[0])){
			$bbandsw[] = null;
		}
		else {
			$bbandsw[] = round(($bbandsEl[1]-$bbandsEl[2])/$bbandsEl[0], 4);
		}
	}
	return array_reverse($bbandsw);
}



//Стандартное отклонение
function standartDeviation($numarray, $sma, $period, $offset=null){
	if($offset!=null)$offsetIter = $offset;
	else $offsetIter = 0;

	//$numArray = array_reverse($numArray);
	$sddata = array();
	for($i=0; $i<sizeof($numarray); $i++){

		$sd = null;

		if($i>=($offsetIter+$period-1)){

			$sum = 0;
			for($m=($period-1); $m>=0; $m--){
				$substracted = $numarray[$i-$m] - $sma[$i];
				$sum += $substracted*$substracted;
			}
			$sd = sqrt($sum/$period);
		}

		$sddata[$i] = $sd;

	}

	return $sddata;
}


//BBands %
function ohclv_bbands($ohclv, $period, $multiplyer, $offset=null){
	if($offset!=null)$offsetIter = $offset;
	else $offsetIter = 0;

	$ohclv = array_reverse($ohclv);
	$osize = sizeof($ohclv);

	//делаем выборку только цен закрытия
	$closeArray = array();
	for($i=0; $i<$osize; $i++){
		$closeArray[] = $ohclv[$i][4];
	}

	$ohlcvSma = simpleParam($closeArray, $period); //moving average
	//$ohlcvSma = waighParam($closeArray, $period); //moving average
	$standartDeviations = standartDeviation($closeArray, $ohlcvSma, $period); //стандартное отклонение

	$bbands = array();
	$bottomBband = array();

	for($i=0; $i<$osize; $i++){
		$upperBbandItem = null;
		$bottomBbandItem = null;

		if($i>=($offsetIter+$period-1)){
			$upperBbandItem = $ohlcvSma[$i]+$multiplyer*$standartDeviations[$i];
			$bottomBbandItem = $ohlcvSma[$i]-$multiplyer*$standartDeviations[$i];
		}

		$bbands[] = array($ohlcvSma[$i], $upperBbandItem, $bottomBbandItem);
	}

	return array_reverse($bbands);

}


//Полосы болинджера Bbands %B
function ohclv_bbandsB($ohclv, $period, $multiplyer, $offset=null){
	if($offset!=null)$offsetIter = $offset;
	else $offsetIter = 0;

	//по цене закрытия подсчет идет
	$bbands = ohclv_bbands($ohclv, $period, $multiplyer, $offset);

	$ohclv = array_reverse($ohclv);
	$osize = sizeof($ohclv);
	$bbands = array_reverse($bbands);

	$bbandB = array();
	for($i=0; $i<$osize; $i++){
		$bbandBIter = null;

		if($i>=($offsetIter+$period-1)){
			//считаем по цене закрытия!
			$znam = ($bbands[$i][1]-$bbands[$i][2]);
			if($znam>0)$bbandBIter = round(($ohclv[$i][4] - $bbands[$i][2])/($bbands[$i][1]-$bbands[$i][2]), 2);
			else $bbandBIter = null;
		}

		$bbandB[] = $bbandBIter;
	}


	return array_reverse($bbandB);
}



//высчитывание простой усредненной Simple MA
function simpleParam($numArray, $period, $offset=null){
	if($offset!=null)$offsetIter = $offset;
	else $offsetIter = 0;

	//$numArray = array_reverse($numArray);
	$smadata = array();
	for($i=0; $i<sizeof($numArray); $i++){

		$sma = null;

		if($i>=($offsetIter+$period-1)){

			$sum = 0;
			for($m=($period-1); $m>=0; $m--){
				$sum += $numArray[$i-$m];
			}
			$sma = $sum/$period;
		}

		$smadata[$i] = $sma;

	}

	return $smadata;
}


//высчитывание экспоненциальной усредненной Exponential MA
function exponentialParam($numArray, $period, $offset=null){

	$smaArray = simpleParam($numArray, $period, $offset);
	$smasizeof = sizeof($smaArray);
	$Kef = 2/($period+1);

	$ema = array();
	for($i=0; $i<$smasizeof; $i++){
		$emaIter = null;

		if($smaArray[$i]!==null){
			//если первое значение, то ставим равно сма
			if($ema[$i-1]===null){
				$emaIter = $smaArray[$i];
			}
			//если не первое - высчитываем
			else {
				$emaIter = $numArray[$i]*$Kef + $ema[$i-1]*(1-$Kef);
			}
		}
		$ema[] = $emaIter;
	}

	return $ema;
}


//RMA для RSI из tradingView - Rolling MA
function rollingParam($numArray, $period, $offset=null){

	$smaArray = simpleParam($numArray, $period, $offset);
	$smasizeof = sizeof($smaArray);
	$Kef = 1/$period;

	$ema = array();
	for($i=0; $i<$smasizeof; $i++){
		$emaIter = null;

		if($smaArray[$i]!==null){
			//если первое значение, то ставим равно сма
			if($ema[$i-1]===null){
				$emaIter = $smaArray[$i];
			}
			//если не первое - высчитываем
			else {
				$emaIter = $numArray[$i]*$Kef + $ema[$i-1]*(1-$Kef);
			}
		}
		$ema[] = $emaIter;
	}

	return $ema;
}


//Smoothed MA
function smoothedParam($numArray, $period, $offset=null){
	if($offset!=null)$offsetIter = $offset;
	else $offsetIter = 0;

	//$numArray = array_reverse($numArray);
	$smmadata = array();
	for($i=0; $i<sizeof($numArray); $i++){

		$smma = null;

		if($i>=($offsetIter+$period-1)){

			//если первый элемент, то
			if($i==($offsetIter+$period-1)){
				$sum = 0;
				for($m=($period-1); $m>=0; $m--){
					$sum += $numArray[$i-$m];
				}
				$smma = $sum/$period;

			}
			//если последующие
			else {
				$smma = ($smmadata[$i-1]*($period-1)+$numArray[$i])/$period;
			}

		}

		$smmadata[$i] = $smma;

	}

	//print_r($smmadata);

	return $smmadata;
}




//высчитывание взвешанной усредненной Weighted MA
function waightedParam($numArray, $period, $offset=null){
	if($offset!==null)$offsetIter = $offset;
	else $offsetIter = 0;


	$wmadata = array();
	for($i=0; $i<sizeof($numArray); $i++){

		$wma = null;

		if($i>=($offsetIter+$period-1)){
			$sumw = 0;
			$sumznm = 0;

			for($m=$period; $m>0; $m--){

				$sumw += $numArray[$i-($period-$m)]*$m;
				$sumznm += $m;
			}

			$wma = $sumw/$sumznm;
		}

		$wmadata[] = $wma;
	}

	return $wmadata;
}

			
			
