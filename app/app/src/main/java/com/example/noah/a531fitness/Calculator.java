package com.example.noah.a531fitness;

import java.util.ArrayList;
import java.util.HashMap;

public class Calculator {
    private int day;
    private int week;
    private int bar_weight = 45;
    private ArrayList<Float> weights;
    private HashMap<String, Float> trainingMax;
    private ArrayList<ArrayList<Float>> weekMultipliers;
    public ArrayList<ArrayList<String>> dayLifts;

    public Calculator(){
        day = 0;
        week = 0;
        trainingMax = new HashMap<>();
        dayLifts = new ArrayList<>();
        dayLifts.add(new ArrayList<String>());
        dayLifts.add(new ArrayList<String>());
        dayLifts.add(new ArrayList<String>());
        weights = new ArrayList<>();
        weights.add(45f);
        weights.add(25f);
        weights.add(10f);
        weights.add(5f);
        weights.add(2.5f);

        weekMultipliers = new ArrayList<>();
        ArrayList<Float> week1 = new ArrayList<>();
        week1.add(0.65f);
        week1.add(0.75f);
        week1.add(0.85f);
        week1.add(0.65f);
        ArrayList<Float> week2 = new ArrayList<>();
        week2.add(0.7f);
        week2.add(0.8f);
        week2.add(0.9f);
        week2.add(0.7f);
        ArrayList<Float> week3 = new ArrayList<>();
        week3.add(0.75f);
        week3.add(0.85f);
        week3.add(0.95f);
        week3.add(0.75f);
        weekMultipliers.add(week1);
        weekMultipliers.add(week2);
        weekMultipliers.add(week3);
    }

    public void addLift(int day, Float max, String name){
        trainingMax.put(name, max);
        dayLifts.get(day).add(name);
    }

    public int getBar_weight() {
        return bar_weight;
    }

    public int getDay() {
        return day;
    }

    public int getWeek() {
        return week;
    }

    public void setBar_weight(int bar_weight) {
        this.bar_weight = bar_weight;
    }

    public void setDay(int day) {
        this.day = day;
    }

    public void setWeek(int week) {
        this.week = week;
    }
}
