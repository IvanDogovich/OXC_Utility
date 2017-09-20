<?PHP
/** Load all Rulesets **/
$library = new MyDirectory("source/xcom1");
//$library = new MyDirectory("source/EleriumFlares");

foreach ($library->Contents as $key=>$file)
{
	if (!((isset($file['Extension']) && $file['Extension'] != 'rul') || $file['Type'] == 'Directory'))
	{
		$library->Contents[$file['Name']] = $file;
	}
	unset($library->Contents[$key]);

}

function cloneSoldiers(&$YAML)
{
	$counts    = array();
    $newlyDead = array();

    $newSoldier = array(
        'type' => 'STR_SOLDIER_S',
        'costBuy' => 20000,
        'costSalary' => 5000,
        'minStats' => array( 
            'tu' => 60,
            'stamina' => 30,
            'health' => 40,
            'bravery' => 10,
            'reactions' => 40,
            'firing' => 40,
            'throwing' => 40,
            'strength' => 10,
            'psiStrength' => 25,
            'psiSkill' => 0,
            'melee' => 30),
        'maxStats' => array(
            'tu' => 80,
            'stamina' => 80,
            'health' => 60,
            'bravery' => 70,
            'reactions' => 70,
            'firing' => 70,
            'throwing' => 65,
            'strength' => 50,
            'psiStrength' => 60,
            'psiSkill' => 0,
            'melee' => 90));

    /* Pull out uncloned soldiers from the death list */
	foreach ($YAML['deadSoldiers'] AS $key=>$soldier)
	{						
		/** Remove numbering for accurate counts **/		
		$pattern = '/ \d+$/';
		$name = str_replace('..', '', preg_replace($pattern, '', $soldier['name']));

		echo $name;
		if (!isset($counts[$name]))
		{
			$counts[$name] = 0;
		}
		$counts[$name] += 1;		

		if (stripos($soldier['name'], '..') === false)
		{
			$newlyDead[$key] = $name;
			$YAML['deadSoldiers'][$key]['name'] = $name;
		}		
	}

	foreach($newlyDead as $key=>$name)
	{
		$total = 0;
		$soldier = $YAML['deadSoldiers'][$key];
		
		/** Update Soldier Count **/
		if (isset($counts[$name]))
		{
			$soldier['name'] .= " ".($counts[$name] + 1);	
		}

		/** Reset Rank, Death, and Armor **/
		$soldier['rank']  = 0;
        $soldier['armor'] = "STR_ADVENTURER_OUTFIT_UC";

		unset($soldier['death']);

		/** Update Stats **/        
        if (stripos($soldier['name'], '~') !== false)
        {
            /** TODO: Read Rulesets for stat limits **/
            foreach ($soldier['currentStats'] AS $stat=>$value)
            {
                $newValue = rand($newSoldier['minStats'][$stat], $newSoldier['maxStats'][$stat]);
                if ($stat == 'bravery')
                {
                    $newValue = round($newValue, -1);
                }
                $soldier['initialStats'][$stat] = $soldier['currentStats'][$stat] = $newValue;
            }
            
            $soldier['recovery'] = 0;
            $soldier['missions'] = 0;
            $soldier['lookVariant'] = rand(0,16);           
            $soldier['kills'] = 0;

            unset($soldier['diary']);

        }
        else
        {
            foreach ($soldier['currentStats'] AS $stat=>$value)
            {
                if (stripos($stat, 'psi') !== false || stripos($stat, 'bravery') !== false)
                {
                    continue;
                }

                $diff = round((abs($value - $soldier['initialStats'][$stat]) * 0.60), 0, PHP_ROUND_HALF_UP);
                $total += $diff;
                $soldier['currentStats'][$stat] = $soldier['initialStats'][$stat] + $diff;
            }

            /** OLD: Give wounds proportional to stats lost 7-42 **/
            /** Give wounds based on health restored as per X-COM, giving first 20 health for free **/
            $health = $soldier['currentStats']['health'];
            $soldier['recovery'] = round(rand($health*0.5, $health*1),0);
            
            if ($soldier['recovery'] < 7) 
            {
                $soldier['recovery'] = 7;
            }
            /*
            else if ($soldier['recovery'] > 42) 
            {
                $soldier['recovery'] = 42;
            }*/

            /** Update Diary Days Wounded **/
            if ($soldier['recovery'] > 0)
            {
                if (!isset($soldier['diary']['daysWoundedTotal']))
                {
                    $soldier['diary']['daysWoundedTotal'] = 0;
                }
                $soldier['diary']['daysWoundedTotal'] += $soldier['recovery'];
            }
        }

		/** Charge for Cloning **/
		$funds = end($YAML['funds']);
		$index = key($YAML['funds']);

		$YAML['funds'][$index] -= ($soldier['recovery']*1000);


		/** update original death array to note their cloned status **/
		$YAML['deadSoldiers'][$key]['name'] = "..".$YAML['deadSoldiers'][$key]['name'];

		/* Add to primary base (replace clones later) */
		$YAML['bases'][0]['soldiers'][] = $soldier;		
		unset($soldier);
	}
}

function battleStats($YAML)
{
    if (!isset($YAML['mission']))
    {
        return false;
    }

    $info['turn'] = $YAML['turn'];

    foreach($YAML['battleGame']['units'] AS $key=>$unit)
    {
        if ($unit['murdererId'] != 0)
        {
            if (!isset($info['score'][$unit['faction']]))
            {
                $info['score'][$unit['faction']] = 0;
            }
            $info['score'][$unit['faction']]++;
        }
    }
    return $info;
    FB::log($info);
}


//$save = new YAML('//IVYBRIDGE/OpenXcom - Extended/user/xcom2/_autobattle_.asav');

//battleStats($save->YAMLArray);
//exit();
$basedir  = '//IVYBRIDGE/OpenXcom - XPiratez/user/';
$xcom     = 'piratez';


$save = new YAML($basedir.$xcom.'/End of Stream.sav');

cloneSoldiers($save->YAMLArray);

/* change the save-file name */
$save->YAMLArray['name'] = 'Fresh Clones';
$save->saveFile($basedir.$xcom.'/'.$save->YAMLArray['name'].'.sav');
?>
