<?php

$user_agent_predefini = "Jhonson";


if (isset($_SERVER['HTTP_USER_AGENT'])) {
    $user_agent_actuel = $_SERVER['HTTP_USER_AGENT'];

    
    if ($user_agent_actuel === $user_agent_predefini) {
        
        echo "L'en-tête User-Agent correspond à la valeur prédéfinie. ✅";
    } else {
       
        echo "L'en-tête User-Agent est incorrect. ❌";
    }
} else {
   
    echo "Erreur : L'en-tête User-Agent n'est pas présent dans la requête.";
}
?>
